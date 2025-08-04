# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Booking
from schemas import BookingRequest, BookingResponse
from datetime import timedelta, datetime, time
from typing import Dict, List

Base.metadata.create_all(bind=engine)

app = FastAPI()

# In-memory session store per client (use Redis or DB in prod)
user_sessions: Dict[str, Dict] = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_session(client_name: str):
    if client_name in user_sessions:
        del user_sessions[client_name]

def parse_time_from_message(message: str) -> datetime | None:
    # Dummy example, replace with proper NLP/time parser like dateparser
    # For demo, expect format "YYYY-MM-DD HH:MM"
    try:
        dt = datetime.strptime(message.strip(), "%Y-%m-%d %H:%M")
        return dt if dt > datetime.now() else None
    except Exception:
        return None

def suggest_available_slots(db: Session, count: int = 3) -> List[datetime]:
    now = datetime.now()

    # Working hours
    work_start = time(9, 0)
    work_end = time(19, 0)
    slot_duration = timedelta(minutes=30)

    # Round current time up to next half hour slot
    start_dt = now.replace(second=0, microsecond=0)
    minute = ((start_dt.minute // 30) + 1) * 30
    if minute == 60:
        start_dt = start_dt.replace(hour=start_dt.hour + 1, minute=0)
    else:
        start_dt = start_dt.replace(minute=minute)

    slots_found = []
    max_days_ahead = 7  # look 7 days ahead

    for day_offset in range(max_days_ahead):
        day = start_dt.date() + timedelta(days=day_offset)
        day_start_dt = datetime.combine(day, work_start)
        day_end_dt = datetime.combine(day, work_end)
        last_slot_start = day_end_dt - slot_duration

        current_time = day_start_dt
        # If today, start from start_dt (rounded current time)
        if day == start_dt.date():
            current_time = max(day_start_dt, start_dt)

        while current_time <= last_slot_start:
            # Check for booking conflicts
            conflict = db.query(Booking).filter(
                Booking.start_time < current_time + slot_duration,
                Booking.end_time > current_time
            ).first()
            if not conflict:
                slots_found.append(current_time)
                if len(slots_found) >= count:
                    return slots_found
            current_time += slot_duration

    return slots_found

@app.post("/chat", response_model=BookingResponse)
def chat_bot(req: BookingRequest, db: Session = Depends(get_db)):
    message = req.message.lower()
    client_name = req.client_name or "Guest"
    session = user_sessions.get(client_name, {"state": "start", "data": {}})

    # Helper: Save session state & data
    def update_session(state=None, data=None):
        if state:
            session["state"] = state
        if data:
            session["data"].update(data)
        user_sessions[client_name] = session

    # 1. Greeting
    greetings = ["hi", "hello", "hey"]
    if any(greet in message for greet in greetings) and session["state"] == "start":
        update_session(state="awaiting_service")
        return {"response": f"Welcome to Salon Deluxe, {client_name}! How can I assist you today? Haircut, shaving, or another service?"}

    # 2. Service Selection
    if session["state"] == "awaiting_service":
        services = ["haircut", "shaving", "beard trimming", "manicure", "pedicure", "styling"]
        selected_services = [s for s in services if s in message]
        if selected_services:
            update_session(state="awaiting_datetime", data={"services": selected_services})
            return {"response": f"Great! You selected {', '.join(selected_services)}. What date and time would you prefer? (Format: YYYY-MM-DD HH:MM)"}
        else:
            return {"response": "Sorry, I didn't catch the service. Please tell me which service you'd like: haircut, shaving, beard trimming, manicure, etc."}

    # 3. Date and Time Inquiry
    if session["state"] == "awaiting_datetime":
        desired_time = parse_time_from_message(message)
        if not desired_time:
            slots = suggest_available_slots(db)
            if not slots:
                return {"response": "Sorry, no available slots soon. Would you like to join the waitlist?"}
            slots_str = ", ".join(slot.strftime("%A %I:%M %p") for slot in slots)
            return {"response": f"We have availability: {slots_str}. Please choose a preferred date and time. (Format: YYYY-MM-DD HH:MM)"}
        else:
            update_session(state="awaiting_confirmation", data={"desired_time": desired_time})
            readable_time = desired_time.strftime("%A %I:%M %p")
            return {"response": f"Booking for {readable_time}. Please provide your full name and phone number to confirm."}

    # 4. Booking Confirmation
    if session["state"] == "awaiting_confirmation":
        data = session["data"]
        if "name" not in data or "phone" not in data:
            if any(char.isdigit() for char in message):
                update_session(data={"phone": message.strip()})
                return {"response": "Thanks for the phone number. Please provide your full name."}
            else:
                update_session(data={"name": message.strip()})
                if "phone" not in data:
                    return {"response": "Thanks! Now please provide your phone number."}

        if "name" in data and "phone" in data:
            services_str = ", ".join(data.get("services", ["service"]))
            desired_time = data["desired_time"]
            new_booking = Booking(
                client_name=data["name"],
                service=services_str,
                start_time=desired_time,
                end_time=desired_time + timedelta(minutes=30),
            )
            db.add(new_booking)
            db.commit()
            reset_session(client_name)
            return {"response": f"✅ Your appointment for {services_str} on {desired_time.strftime('%A %I:%M %p')} is confirmed. Thank you, {data['name']}!"}

        return {"response": "Please provide your full name and phone number to confirm booking."}

    # 5. Modification or Cancellation
    if "change my booking" in message or "reschedule" in message or "modify" in message:
        booking = db.query(Booking).filter(Booking.client_name == client_name).order_by(Booking.start_time.desc()).first()
        if not booking:
            return {"response": "You have no existing bookings to modify."}
        new_time = parse_time_from_message(message)
        if not new_time:
            return {"response": "Please specify the new date and time you want to reschedule to."}
        booking.start_time = new_time
        booking.end_time = new_time + timedelta(minutes=30)
        db.commit()
        return {"response": f"Your appointment has been updated to {new_time.strftime('%A %I:%M %p')}."}

    if "cancel my booking" in message or "delete my booking" in message:
        booking = db.query(Booking).filter(Booking.client_name == client_name).order_by(Booking.start_time.desc()).first()
        if not booking:
            return {"response": "You have no existing bookings to cancel."}
        db.delete(booking)
        db.commit()
        return {"response": "Your appointment has been cancelled."}

    # 6. Price Inquiry
    if "price" in message or "cost" in message or "how much" in message:
        return {"response": "Haircuts start at $20. Would you like to book an appointment?"}

    # 7. Additional Services
    if "beard trimming" in message:
        return {"response": "Yes, we do beard trimming. Would you like to add it to your booking?"}

    # 8. Special Requests
    if "experienced stylist" in message or "stylist john" in message:
        return {"response": "Noted! We’ll assign a stylist matching your preference."}

    # 9. Location and Hours
    if "where" in message or "location" in message or "address" in message:
        return {"response": "We’re at 123 Main Street, Downtown. Open 9 AM to 7 PM daily."}

    # 10. Farewell
    farewells = ["thanks", "thank you", "bye", "goodbye"]
    if any(farewell in message for farewell in farewells):
        reset_session(client_name)
        return {"response": "Thanks for choosing us! Have a great day."}

    # 11. Membership and Discounts
    if "discount" in message or "membership" in message:
        return {"response": "Members get 10% off. Do you want to apply your membership?"}

    # 12. Multiple Bookings (basic)
    if "book" in message and "and" in message:
        return {"response": "Booking multiple services at once is coming soon! Please book one service at a time for now."}

    # 13. Waitlist Management
    if "waitlist" in message:
        return {"response": "Sure, I’ve added you to the waitlist. We’ll notify you if a slot opens up."}

    # 18. Covid-19 Safety
    if "covid" in message or "protocol" in message or "safety" in message:
        return {"response": "Yes, we follow Covid-19 safety protocols: masks, sanitizing, and social distancing."}

    # 29. Bot Handoff to Human Agent
    if "talk to a person" in message or "human" in message or "representative" in message:
        return {"response": "Connecting you to a representative. Please wait..."}

    # Default fallback
    return {"response": "I'm sorry, I didn't understand that. You can ask to book an appointment, check available slots, or inquire about our services."}
