# schemas.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    selected_text: str | None = None

class ChatResponse(BaseModel):
    answer: str
