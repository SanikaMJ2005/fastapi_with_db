from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from db import get_db, DATABASE_URL
from sqlalchemy import create_engine
from models import Base
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Enable CORS so your React frontend (localhost:5173) can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)

# Create database tables on startup
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"status": "Server is running", "message": "Welcome to the Singnup API"}

if __name__ == "__main__":
    # Use "main:app" string format to allow reload to work properly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)