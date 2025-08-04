# utils.py
from datetime import datetime, timedelta
import re
from models import Booking  # Required to query bookings

def parse_time_from_message(message: str):
    message = message.lower()

    # Simple keywords
    if "tomorrow" in message:
        base_date = datetime.now() + timedelta(days=1)
    elif "today" in message:
        base_date = datetime.now()
    elif "now" in message:
        return datetime.now()
    else:
        base_date = None

    # Map weekdays to integer
    days_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }

    # Regex to find time like 9, 9:00, 09:30 am, etc.
    time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'

    # Find weekday in message
    found_day = None
    for day_name in days_map:
        if day_name in message:
            found_day = day_name
            break

    # Find time in message
    time_match = re.search(time_pattern, message)

    if found_day and time_match:
        today = datetime.now()
        target_weekday = days_map[found_day]

        # Calculate how many days until the target weekday
        days_ahead = target_weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        target_date = today + timedelta(days=days_ahead)

        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        ampm = time_match.group(3)

        # Convert to 24h format
        if ampm == 'pm' and hour != 12:
            hour += 12
        elif ampm == 'am' and hour == 12:
            hour = 0

        return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Fallback to base_date with default 9AM time if keyword found
    if base_date:
        return base_date.replace(hour=9, minute=0, second=0, microsecond=0)

    return None

def suggest_available_slots(db):
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    slots = []
    for i in range(20):  # 10 hours in 30-min increments
        slot = base_time + timedelta(minutes=30*i)
        existing = db.query(Booking).filter(Booking.start_time == slot).first()
        if not existing:
            slots.append(slot)
        if len(slots) == 3:
            break
    return slots


