from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from supabase import create_client, Client

from .chatbot import generate_response
from .config import settings


app = FastAPI(
    title="Cafe De Flora AI Assistant",
    description="AI-powered customer support chatbot",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------
# SUPABASE
# ---------------------------------

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)


# ---------------------------------
# REQUEST MODELS
# ---------------------------------

class ChatRequest(BaseModel):
    message: str


class FeedbackRequest(BaseModel):
    message: str
    bot_response: str
    rating: int
    reason: Optional[str] = None
    comment: Optional[str] = None


# ---------------------------------
# HOME
# ---------------------------------

@app.get("/")
def home():
    return {
        "message": "Cafe De Flora AI Assistant is running!"
    }


# ---------------------------------
# HEALTH
# ---------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------------------------
# CHAT
# ---------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    response = generate_response(request.message)

    return {
        "message": request.message,
        "response": response
    }


# ---------------------------------
# FEEDBACK
# ---------------------------------

@app.post("/feedback")
def feedback(request: FeedbackRequest):

    # Validate rating
    if request.rating < 1 or request.rating > 5:
        return {
            "success": False,
            "message": "Rating must be between 1 and 5."
        }

    # Low ratings require a reason
    if request.rating <= 2 and not request.reason:
        return {
            "success": False,
            "message": "Please provide a reason for a low rating."
        }

    try:

        data = {
            "message": request.message,
            "bot_response": request.bot_response,
            "rating": request.rating,
            "reason": request.reason,
            "comment": request.comment
        }

        result = supabase.table("feedback").insert(data).execute()

        return {
            "success": True,
            "message": "Thank you for your feedback!"
        }

    except Exception as e:

        print("Feedback error:", e)

        return {
            "success": False,
            "message": "Unable to save feedback at the moment."
        }