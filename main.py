import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from dotenv import load_dotenv

# --- CRITICAL: LOAD ENV FIRST ---
load_dotenv() 

# Import routes and local files AFTER loading env
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from db import DATABASE_URL
from models import Base

# Initialize FastAPI app
app = FastAPI(title="Project AI Backend")

# 1. DEBUG CHECK (Check your terminal when you save this!)
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("❌ ERROR: GITHUB_TOKEN is not being read from .env!")
else:
    # Prints the first few characters to verify it's the right one
    print(f"✅ SUCCESS: GITHUB_TOKEN loaded (Starts with: {token[:7]}...)")

# 2. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Database Table Creation
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# 4. Include Routers
app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)

@app.get("/")
def read_root():
    return {
        "status": "Server is online", 
        "token_detected": True if token else False,
        "message": "Welcome to the API"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)