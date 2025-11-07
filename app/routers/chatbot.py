from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.customer import Customer

router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])

class ChatRequest(BaseModel):
    customer_id: int
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool

# Predefined Q&A mapping
PREDEFINED_QA = {
    "Why is my service blocked?": "Your service is blocked because your account has an overdue balance. Please pay the outstanding amount to restore your service.",
    "Why is my data speed restricted?": "Your data speed is restricted due to an unpaid bill. Once the payment is made, your data speed will be restored.",
    "When is my payment due?": "You can view your payment due date on your dashboard. Please pay before the due date to avoid service restrictions.",
    "How much do I owe?": "Please check your account dashboard for the current outstanding balance.",
    "How to restore my service?": "To restore your service, please pay any overdue bills. Your account will be updated once payment is confirmed.",
    "What does account status mean?": "Your account status reflects your payment and usage activity. ACTIVE means your account is in good standing. RESTRICTED or BARRED means action is needed.",
    # Add more Q&A pairs as needed
}

@router.post("/query", response_model=ChatResponse)
def chatbot_query(request: ChatRequest, db: Session = Depends(get_db)):
    question = request.message.strip()
    answer = PREDEFINED_QA.get(question)

    # Fallback to generic response if question not found
    if not answer:
        answer = "I'm sorry, I did not understand your question. Please ask about your service, payment, or account status."

    return ChatResponse(response=answer, success=True)
