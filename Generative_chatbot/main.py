from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlite3
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Salon Booking Chatbot", version="1.0.0")

# OpenAI client setup
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database setup
DATABASE_PATH = os.getenv("DATABASE_PATH", "salon_bookings.db")

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            service TEXT NOT NULL,
            start_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

# Pydantic models
class UserMessage(BaseModel):
    user_id: str
    message: str

class BookingRequest(BaseModel):
    user_id: str
    service: str
    start_time: str

class ChatResponse(BaseModel):
    reply: str

def parse_intent_entities(message: str):
    """Parse user message to extract intent and entities using OpenAI"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI assistant for a salon booking system. 
                    Analyze the user message and extract:
                    1. Intent: greeting, ask_services, book_appointment, check_slots, cancel_appointment, unknown
                    2. Service: haircut, hair_wash, facial (if mentioned)
                    3. Time: any time mentioned (optional)
                    
                    Return ONLY a JSON object with: {"intent": "...", "service": "...", "time": "..."}
                    If no service/time found, use null."""
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        print(f"Raw GPT response: {result}")
        
        # Parse JSON response
        import json
        parsed = json.loads(result)
        return parsed
    except Exception as e:
        print(f"Error parsing intent: {e}")
        return {"intent": "unknown", "service": None, "time": None}

def get_sample_slots():
    """Generate sample available time slots"""
    slots = []
    start_hour = 9  # 9 AM
    end_hour = 17   # 5 PM
    
    for hour in range(start_hour, end_hour):
        slots.append(f"{hour:02d}:00")
        slots.append(f"{hour:02d}:30")
    
    return slots

@app.get("/")
async def root():
    return {"message": "AI Salon Booking Chatbot API"}

@app.post("/chat/message", response_model=ChatResponse)
async def chat_message(user_message: UserMessage):
    """Handle chat messages and provide human-like responses"""
    
    # Parse intent and entities
    parsed = parse_intent_entities(user_message.message)
    intent = parsed.get("intent", "unknown")
    service = parsed.get("service")
    time = parsed.get("time")
    
    print(f"Parsed: intent={intent}, service={service}, time={time}")
    
    # Generate appropriate response based on intent
    if intent == "greeting":
        reply = "Hello! 👋 Welcome to our salon! I'm here to help you with bookings and services. How can I assist you today?"
    
    elif intent == "ask_services":
        reply = """Great question! Here are the services we offer:

• Haircut (60 minutes)
• Hair Wash (30 minutes)  
• Facial (45 minutes)

What would you like to book today?"""
    
    elif intent == "book_appointment":
        if service:
            available_slots = get_sample_slots()
            slots_text = ", ".join(available_slots[:6])  # Show first 6 slots
            reply = f"Perfect! I'd be happy to book a {service} for you. Here are some available times: {slots_text}. What time works best for you?"
        else:
            reply = "I'd be happy to help you book an appointment! What service would you like? We offer haircuts, hair wash, and facials."
    
    elif intent == "check_slots":
        available_slots = get_sample_slots()
        slots_text = ", ".join(available_slots[:8])  # Show first 8 slots
        reply = f"Here are our available time slots: {slots_text}. What time would you prefer?"
    
    else:
        reply = "I'm not sure I understood that. Could you please let me know if you'd like to see our services, book an appointment, or check available times?"
    
    return ChatResponse(reply=reply)

@app.post("/booking")
async def create_booking(booking: BookingRequest):
    """Create a new booking"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bookings (user_id, service, start_time)
            VALUES (?, ?, ?)
        ''', (booking.user_id, booking.service, booking.start_time))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "message": "Booking created successfully",
            "booking_id": booking_id,
            "user_id": booking.user_id,
            "service": booking.service,
            "start_time": booking.start_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")

@app.get("/bookings")
async def get_all_bookings():
    """Get all bookings"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bookings ORDER BY created_at DESC')
        bookings = cursor.fetchall()
        
        conn.close()
        
        return {
            "bookings": [
                {
                    "id": booking[0],
                    "user_id": booking[1],
                    "service": booking[2],
                    "start_time": booking[3],
                    "created_at": booking[4]
                }
                for booking in bookings
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {str(e)}")

@app.get("/bookings/{user_id}")
async def get_user_bookings(user_id: str):
    """Get bookings for a specific user"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bookings WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        bookings = cursor.fetchall()
        
        conn.close()
        
        return {
            "user_id": user_id,
            "bookings": [
                {
                    "id": booking[0],
                    "user_id": booking[1],
                    "service": booking[2],
                    "start_time": booking[3],
                    "created_at": booking[4]
                }
                for booking in bookings
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user bookings: {str(e)}")

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: int):
    """Delete a booking by ID"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Booking not found")
        
        conn.commit()
        conn.close()
        
        return {"message": f"Booking {booking_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting booking: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 