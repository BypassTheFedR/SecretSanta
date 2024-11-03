from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .models import FamilyParticipant
from .scheduler import run_assignments
from .email_utils import send_assignments

router = APIRouter()

# Load Jinja2 Template
templates = Jinja2Templates(directory="app/templates")

# In-memory storage for testing
# registered_families = {}
registered_families = {
  "chantalthornburg@gmail.com": {
    "name": "serenity",
    "spouse_name": "nick",
    "spouse_email": "nick@mail.com",
    "children": "Blake,Lyla"
  },
  "joshuarthornburg@gmail.com": {
    "name": "josh",
    "spouse_name": "chantal",
    "spouse_email": "chantal@mail.com",
    "children": "Ayden,Daphne,Chloe"
  },
  "chantaljenson@gmail.com": {
    "name": "cate",
    "spouse_name": "billy",
    "spouse_email": "billy@mail.com",
    "children": "Elizabeth,Rileigh,Junior"
  }
}

# assigned_adults = {}
# assigned_children = {}
# Using assigned dicinoaries as globals
assigned_adults = None
assigned_children = None
adult_pool = None
child_pool = None

def populate_pools(registered_families):
    adult_pool = {}
    child_pool = {}

    # Populate adult_pool with unique IDs for each person and spouse in one loop
    auto_increment_id = 1
    for key, value in registered_families.items():
        # Add primary person
        adult_pool[auto_increment_id] = (value["name"], key, key)
        auto_increment_id += 1
        # Add spouse
        if value.get("spouse_name") and value.get("spouse_email"):
            adult_pool[auto_increment_id] = (value["spouse_name"], value["spouse_email"], key)
            auto_increment_id += 1

    auto_increment_id = 1

    # Populate child_pool, ensuring each child has a unique ID
    for key, value in registered_families.items():
        children = [child.strip() for child in value["children"].split(",")]
        for child in children:
            child_pool[auto_increment_id] = (child, "null", key)
            auto_increment_id += 1

        # Return the populated pools
    return adult_pool, child_pool

@router.get("/register/", response_class=HTMLResponse)
async def get_registration_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register/")
async def register_family(
    name: str = Form(...),
    email: str = Form(...),
    spouse_name: str = Form(None),
    spouse_email: str = Form(None),
    children: str = Form(None)
):
    if email in registered_families:
        raise HTTPException(status_code=400, detail="Family already registered.")
    
    children_list = [child.strip() for child in children.split(",")] if children else []
    
    # Store particpant dat a in memory
    registered_families[email] = {
        "name": name,
        "spouse_name": spouse_name,
        "spouse_email": spouse_email,
        "children": children_list
    }
    # placeholder for saving particpant data
    return {"message" : f"Family registration successful for {name}'s family"}

@router.post("/assignments/")
@router.get("/assignments/")
async def generate_assignments():
    global assigned_adults, assigned_children, adult_pool, child_pool
    try:
        if not registered_families:
            raise HTTPException(status_code=400, detail="No families registered.")
        
        # Use populate_pools to create adult_pool and child_pool
        adult_pool, child_pool = populate_pools(registered_families)

        # Generate assignments for adults and children
        assigned_adults, assigned_children = run_assignments(adult_pool, child_pool)

        # Redirect to send_emails_page for confirmation
        return RedirectResponse(url=f"/send_emails_page", status_code=303)
        
    except Exception as e:
        # Redirect to the admin page if the assignment's couldn't be made
        return RedirectResponse(url="/admin?error=assignment_failed", status_code=303)

@router.get("/families/")
async def get_registered_families():
    return registered_families
    # get_registered_families testing version
    # DELETE before launch
    # adult_pool, child_pool = populate_pools(registered_families)
    # return registered_families, adult_pool, child_pool

@router.get("/admin/", response_class=HTMLResponse)
async def admin_page(request: Request):
    # Initialize messages
    error_message = None

    # Check for success or error
    if request.query_params.get("error") == "assignment_failed":
        error_message = "Assignments could not be completed after multiple attempts, please try again."
        
    return templates.TemplateResponse("admin.html", {"request": request, "error_message": error_message})

@router.get("/send_emails_page", response_class=HTMLResponse)
async def send_emails_page(request: Request):
    if not assigned_adults  or not assigned_children:
    # Create a custom HTML response with a link to redirect to the admin page
        html_content = """
        <html>
            <head>
                <title>Assignments Not Found</title>
            </head>
            <body>
                <h1>No assignments found.</h1>
                <p>Please <a href="/admin">go back to the admin page</a> and generate assignments first.</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=400)
    # Render the page iwth assignments and a confirmation button
    return templates.TemplateResponse("send_emails_page.html",{
        "request" : request,
        "assigned_adults": assigned_adults,
        "assigned_children": assigned_children
    })

@router.post("/send_emails/")
async def send_emails(request: Request):
    if not assigned_adults or not assigned_children:
        raise HTTPException(status_code=400, detail="No assignments found. Please generate assignments.")

    # Send the assignments
    send_assignments(assigned_adults, assigned_children, adult_pool, child_pool)
    
    # Redirect to admin page for confirmation
    return RedirectResponse(url="/admin?success=emails_sent", status_code=303)