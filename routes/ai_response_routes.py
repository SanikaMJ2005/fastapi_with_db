from fastapi import APIRouter, HTTPException
from utils.ai_response import get_completion
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# 1. Request Schema: Matches what Dashboard.jsx sends
class AIRequest(BaseModel):
    prompt: str  
    system_prompt: Optional[str] = "You are a helpful AI assistant."

# 2. Response Schema: Matches what Dashboard.jsx expects (data.response)
class AIResponse(BaseModel):
    response: str

@router.post("/ask", response_model=AIResponse)
async def ask_ai(request: AIRequest):
    """
    Receives prompt from React, calls Azure/GitHub AI, 
    and returns the result.
    """
    try:
        # We pass 'request.prompt' into the 'user_message' parameter of your utility
        result = get_completion(user_message=request.prompt, system_message=request.system_prompt)
        
        # Ensure we return the object in the format the response_model expects
        return AIResponse(response=result)
        
    except Exception as e:
        # This will show up in your Dashboard's 'Error' catch block
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")