from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
from database import SessionLocal, engine
from models import Base, Booking
from schemas import BookingResponse, BookingRequest
from utils import parse_time_from_message, suggest_alternative

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat", response_model=BookingResponse)
def chat_bot(req: BookingRequest, db: Session = Depends(get_db)):
    message = req.message
    client_name = req.client_name

    desired_time = parse_time_from_message(message)
    if not desired_time:
        return {"response": "Sorry, I couldn't understand the time. Please try like '3 PM today'."}

    existing = db.query(Booking).filter(Booking.start_time == desired_time).first()
    if existing:
        alt = suggest_alternative(desired_time)
        return {"response": f"⏰ Sorry, {desired_time.strftime('%I:%M %p')} is taken. How about {alt.strftime('%I:%M %p')}?"}

    new_booking = Booking(
        client_name=client_name,
        service="Haircut",
        start_time=desired_time,
        end_time=desired_time + timedelta(minutes=30)
    )
    db.add(new_booking)
    db.commit()

    return {"response": f"✅ Booked for {client_name} at {desired_time.strftime('%I:%M %p')}!"}

@app.get("/")
async def root():
    return {"message": "Salon Chatbot API is running!"}
