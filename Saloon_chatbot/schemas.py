from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    client_name: Optional[str] = "Guest"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    booking_confirmed: bool
    session_id: Optional[str] = None
