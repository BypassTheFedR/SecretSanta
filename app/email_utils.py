import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from .config import Config, Debug_Config
from .config import Config

def send_email(to_email: str, subject: str, body: str):
    try:
        # Set up the SMTP server
        with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) as server:
            server.starttls() # Start TLS encryption
            server.login(Config.EMAIL_ADDRESS, Config.APP_PASSWORD)

            # Create the email
            msg = MIMEMultipart()
            msg["From"] = Config.EMAIL_ADDRESS
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # send the email
            server.send_message(msg)
            print(f"Email send to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Debug copy of send_email
# def send_email(to_email: str, subject: str, body: str):
#     try:
#         # Set up the SMTP server
#         with smtplib.SMTP(Debug_Config.EMAIL_HOST, Debug_Config.EMAIL_PORT) as server:
#             # server.starttls() # Start TLS encryption
#             # server.login(Debug_Config.EMAIL_ADDRESS, Debug_Config.APP_PASSWORD)

#             # Create the email
#             msg = MIMEMultipart()
#             msg["From"] = Debug_Config.EMAIL_ADDRESS
#             msg["To"] = to_email
#             msg["Subject"] = subject
#             msg.attach(MIMEText(body, "plain"))

#             # send the email
#             server.send_message(msg)
#             print(f"Email send to {to_email}")
#     except Exception as e:
#         print(f"Failed to send email to {to_email}: {e}")

# Sends the pairings to the appropriate email.
def send_assignments(assigned_adults, assigned_children, adult_pool, child_pool):
    # Send emails to each adult
    for giver_name, receiver_name in assigned_adults.items():
        # Find the giver's email
        giver_email = next(data[1] for id, data in adult_pool.items() if data[0] == giver_name)

        # Email content for the adults
        subject = "Your Secret Santa Assignment"
        body = f"Hello, {giver_name}, \n\n You are buying a gift for {receiver_name}!"
        # print(f"\n{giver_email}")
        # print(subject)
        # print(body)
        # print()

        # Send email to adult
        send_email(giver_email, subject, body)
    
    # Prepare and send aggregated assignments for child to each parent
    family_assignments = {}
    for child_giver, child_receiver in assigned_children.items():
        # Retrieve the family email from child_pool
        # parent_email = next(data[2] for id, data in child_pool.items() if data[0] == child_giver and data[1] != "null")
        parent_email = None
        for id, data in child_pool.items():
            if data[0] == child_giver:
                parent_email = data[2]
                break
        if parent_email is None:
            raise ValueError(f"Parent email not found for child {child_giver} in child_pool.")

        # Group child assignments by family email
        if parent_email not in family_assignments:
            family_assignments[parent_email] = []
        family_assignments[parent_email].append(f"{child_giver} is assigned to {child_receiver}")

     # Send one email per family for child assignments
    for parent_email, assignments in family_assignments.items():
        subject = "Your Children's Secret Santa Assignments"
        body = "Hello,\n\nHere are the assignments for your children:\n" + "\n".join(assignments) + "\n\nHappy gifting!"
        
        send_email(parent_email, subject, body)