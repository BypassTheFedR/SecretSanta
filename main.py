##################################################
### Runs the FastAPI, and sets the routes      ###
################################################## 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router as secret_santa_router
from app.config import Config


# Initialize the FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root end point
@app.get("/")
def read_root():
    return {"message": "Welcome to the Secret Santa App!"}

# More routes
# from app.routes import router as secret_santa_router
app.include_router(secret_santa_router)