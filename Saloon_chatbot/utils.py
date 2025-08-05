import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models import Booking

class SalonChatBot:
    def __init__(self):
        self.services = {
            'haircut': {'name': 'Haircut & Styling', 'duration': 60, 'price': 30},
            'hair_wash': {'name': 'Hair Wash & Blow Dry', 'duration': 30, 'price': 15},
            'facial': {'name': 'Facial Treatment', 'duration': 90, 'price': 50},
            'manicure': {'name': 'Manicure', 'duration': 45, 'price': 25},
            'pedicure': {'name': 'Pedicure', 'duration': 60, 'price': 30},
            'massage': {'name': 'Head & Shoulder Massage', 'duration': 45, 'price': 35},
            'eyebrow': {'name': 'Eyebrow Threading', 'duration': 20, 'price': 12},
            'hair_color': {'name': 'Hair Coloring', 'duration': 120, 'price': 80},
            'highlights': {'name': 'Hair Highlights', 'duration': 150, 'price': 100}
        }
        self.conversations = {}

    def get_conversation_state(self, session_id: str) -> Dict:
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'stage': 'greeting',
                'selected_service': None,
                'available_times': [],
                'client_name': 'Guest'
            }
        return self.conversations[session_id]

    def detect_intent(self, message: str, session_id: Optional[str] = None) -> str:
        message = message.lower().strip()
        state = self.get_conversation_state(session_id) if session_id else None

        # Step 1: If we're showing available times, prioritize confirming booking
        if state and state.get('stage') == 'show_times':
            if re.search(r'\b\d+\b', message):
                return 'confirm_booking'

        # Step 2: Handle greetings
        if any(word in message for word in ['hi', 'hello', 'hey']):
            return 'greeting'

        # Step 3: Handle asking about services
        if any(phrase in message for phrase in ['services', 'what do you offer']):
            return 'ask_services'

        # Step 4: Detect service by name
        for key, info in self.services.items():
            if key.replace('_', ' ') in message or info['name'].lower() in message:
                return f'select_service:{key}'

        # Step 5: Detect service by number — ONLY IF NOT in show_times stage
        if state and state.get('stage') != 'show_times':
            if any(word in message for word in ['book', 'appointment', 'schedule']):
                match = re.match(r'book\s+(\d+)', message)
                if match:
                    num = int(match.group(1))
                    if 1 <= num <= len(self.services):
                        return f'select_service_by_number:{num}'
                return 'start_booking'

        # Step 6: Confirm or cancel
        if any(word in message for word in ['confirm', 'yes', 'ok', 'sure']):
            return 'confirm_booking'

        if any(word in message for word in ['cancel', 'no']):
            return 'cancel'

        # Step 7: Fallback
        return 'general'





    def generate_available_times(self, duration: int, db) -> List[Dict]:
        available = []
        now = datetime.now()
        for day_offset in range(2):  # Today and tomorrow
            date = (now + timedelta(days=day_offset)).date()
            start = datetime.combine(date, datetime.min.time().replace(hour=9))
            end = datetime.combine(date, datetime.min.time().replace(hour=19))
            current = start
            while current < end:
                existing = db.query(Booking).filter(Booking.slot_time == current).first()
                if not existing:
                    available.append({'datetime': current, 'display': current.strftime("%A %I:%M %p")})
                current += timedelta(minutes=30)
                if len(available) >= 10:
                    break
        return available

    def chat_response(self, message: str, session_id: str, client_name: str, db) -> Dict:
        state = self.get_conversation_state(session_id)
        state['client_name'] = client_name
        intent = self.detect_intent(message)

        if intent == 'greeting':
            state['stage'] = 'greeting'
            return {'reply': f"Hello {client_name}! Welcome to our salon. How can I help you today?", 'booking_confirmed': False}

        if intent == 'ask_services':
            state['stage'] = 'services'
            return {'reply': self._show_services(), 'booking_confirmed': False}

        if intent.startswith('select_service_by_number:'):
            service_number = int(intent.split(':')[1])
            service_keys = list(self.services.keys())
            if 1 <= service_number <= len(service_keys):
                service_key = service_keys[service_number - 1]
                state['selected_service'] = service_key
                service_info = self.services[service_key]
                times = self.generate_available_times(service_info['duration'], db)
                state['available_times'] = times
                state['stage'] = 'show_times'

                if times:
                    reply = f"Great choice! {service_info['name']} takes {service_info['duration']} mins and costs ${service_info['price']}.\n"
                    reply += self._show_available_times(times)
                    return {'reply': reply, 'booking_confirmed': False}
                else:
                    return {'reply': "Sorry, no slots available right now. Try again later.", 'booking_confirmed': False}
            else:
                return {'reply': "Invalid service number. Please choose a valid service.", 'booking_confirmed': False}

        if intent.startswith('select_service:'):
            service_key = intent.split(':')[1]
            state['selected_service'] = service_key
            service_info = self.services[service_key]
            times = self.generate_available_times(service_info['duration'], db)
            state['available_times'] = times
            state['stage'] = 'show_times'
            if times:
                reply = f"Great choice! {service_info['name']} takes {service_info['duration']} mins and costs ${service_info['price']}.\n"
                reply += self._show_available_times(times)
                return {'reply': reply, 'booking_confirmed': False}
            else:
                return {'reply': "Sorry, no slots available right now. Try again later.", 'booking_confirmed': False}

        if intent == 'confirm_booking' and state['stage'] == 'show_times':
            if not state['selected_service']:
                response = "Please select a service first. Here are our popular services:\n\n" + self._show_services()
                state['stage'] = 'services'
                return {'reply': response, 'booking_confirmed': False}

            selected_time = self._extract_time_selection(message, state['available_times'])
            if selected_time:
                booking = self._create_booking(client_name, state['selected_service'], selected_time, db)
                state['stage'] = 'booked'
                return {'reply': booking, 'booking_confirmed': True}
            else:
                return {'reply': "Please specify a valid time slot to book.", 'booking_confirmed': False}

        if intent == 'cancel':
            self.conversations.pop(session_id, None)
            return {'reply': "Booking cancelled. Let me know if you need anything else.", 'booking_confirmed': False}

        # fallback
        return {'reply': "I'm here to help you book salon appointments! What would you like to do today?", 'booking_confirmed': False}

    def _show_services(self) -> str:
        text = "Here are our services:\n"
        for i, (k, v) in enumerate(self.services.items(), 1):
            text += f"{i}. {v['name']} - ${v['price']} ({v['duration']} mins)\n"
        text += "Which service would you like to book?"
        return text

    def _show_available_times(self, times: List[Dict]) -> str:
        text = "Available slots:\n"
        for i, t in enumerate(times[:8], 1):
            text += f"{i}. {t['display']}\n"
        text += "Please reply with the slot number to book."
        return text

    def _extract_time_selection(self, message: str, times: List[Dict]) -> Optional[datetime]:
        match = re.search(r'\b(\d+)\b', message)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(times):
                return times[idx]['datetime']
        return None

    def _create_booking(self, client_name: str, service_key: str, time: datetime, db) -> str:
        service_info = self.services[service_key]
        booking = Booking(client_name=client_name, service=service_info['name'], slot_time=time, phone="")
        db.add(booking)
        db.commit()
        return (f"Booking confirmed for {service_info['name']} on {time.strftime('%A, %b %d %I:%M %p')}.\n"
                f"Price: ${service_info['price']}. See you then!")

salon_bot = SalonChatBot()
