import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://models.github.ai/inference"
model_name = "gpt-4o-mini"

def get_client():
    # Fetch token fresh each time to ensure it uses the cleaned version
    raw_token = os.getenv("GITHUB_TOKEN", "")
    token = raw_token.strip().strip('"').strip("'")
    
    if not token:
        print("❌ ERROR: GITHUB_TOKEN is empty in environment!")
        return None
        
    return ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

def get_completion(user_message, system_message="You are a helpful assistant."):
    client = get_client()
    if client is None:
        return "Error: Token missing. Check your .env file."

    try:
        response = client.complete(
            messages=[
                SystemMessage(content=system_message),
                UserMessage(content=user_message),
            ],
            model=model_name
        )
        return response.choices[0].message.content
    except Exception as e:
        # LOG THIS TO YOUR TERMINAL
        print(f"--- API ERROR DETAIL ---")
        print(f"Status Code/Message: {str(e)}")
        print(f"------------------------")
        
        if "Unauthorized" in str(e):
            return "AI Error: Unauthorized. Your token needs 'repo' or 'read:packages' scopes on GitHub."
        return f"AI Error: {str(e)}"