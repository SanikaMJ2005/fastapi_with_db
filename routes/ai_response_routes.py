from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from utils.ai_response import get_completion
from utils.jwt_handler import verify_token
from db import get_db
from models import Chat

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependencies
def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return int(payload.get("sub"))

# 1. Request Schema: Matches what Dashboard.jsx sends
class AIRequest(BaseModel):
    prompt: str  
    system_prompt: Optional[str] = "You are a helpful AI assistant."

# 2. Response Schema: Matches what Dashboard.jsx expects (data.response)
class AIResponse(BaseModel):
    response: str

class ChatHistoryResponse(BaseModel):
    id: int
    prompt: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True

@router.post("/ask", response_model=AIResponse)
async def ask_ai(
    request: AIRequest, 
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Receives prompt from React, calls Azure/GitHub AI, 
    saves to DB, and returns the result.
    """
    try:
        # We pass 'request.prompt' into the 'user_message' parameter of your utility
        result = get_completion(user_message=request.prompt, system_message=request.system_prompt)
        
        # Save to database
        new_chat = Chat(
            user_id=user_id,
            prompt=request.prompt,
            response=result
        )
        db.add(new_chat)
        db.commit()
        
        # Ensure we return the object in the format the response_model expects
        return AIResponse(response=result)
        
    except Exception as e:
        # This will show up in your Dashboard's 'Error' catch block
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

@router.get("/history", response_model=List[ChatHistoryResponse])
async def get_history(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Returns the chat history for the authenticated user.
    """
    chats = db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.timestamp.desc()).all()
    return chats