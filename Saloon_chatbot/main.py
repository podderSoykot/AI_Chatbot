from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Booking
from schemas import ChatRequest, ChatResponse
from utils import salon_bot
import uuid

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Salon Chatbot API",
    description="A conversational AI for salon appointment bookings.",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    if not request.session_id:
        request.session_id = str(uuid.uuid4())
    try:
        result = salon_bot.chat_response(
            message=request.message,
            session_id=request.session_id,
            client_name=request.client_name or "Guest",
            db=db
        )
        return ChatResponse(
            reply=result['reply'],
            booking_confirmed=result.get('booking_confirmed', False),
            session_id=request.session_id
        )
    except Exception as e:
        print(f"[Error]: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the chat message.")

@app.get("/")
def home():
    return {
        "message": "Salon Chatbot API is running!",
        "usage": "POST to /chat with your message to start chatting.",
    }

@app.get("/bookings")
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return [
        {
            "id": b.id,
            "client_name": b.client_name,
            "service": b.service,
            "time": b.slot_time.strftime("%Y-%m-%d %H:%M"),
            "created_at": b.created_at.strftime("%Y-%m-%d %H:%M")
        } for b in bookings
    ]
