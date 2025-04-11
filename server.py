from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import base64
import os
from database import get_connection
from signup import facegetting

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ensure upload folder exists
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Request body models
class SignupData(BaseModel):
    firstName: str
    lastName: str
    email: str
    username: str
    image: str

class LoginData(BaseModel):
    image: str

# Routes

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def post_signup(data: SignupData):
    try:
        image_data = data.image  
        image_bytes = base64.b64decode(image_data)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{data.username}_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO user (firstName, lastName, email, username, img) VALUES (%s, %s, %s, %s, %s)"
        values = (data.firstName, data.lastName, data.email, data.username, filepath)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        # Store data to database here if needed

        return {"message": f"Signup successful. Image saved as {filename}"}
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=400)

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(data: LoginData):
    try:
        image_data = data.image.split(',')[1] if ',' in data.image else data.image
        image_bytes = base64.b64decode(image_data)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"login_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # Add face verification here later

        return {"message": f"Login image captured as {filename}"}
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=400)
