import requests
import json

def test_chat_endpoint():
    """Test the chat message endpoint"""
    print("🤖 Testing Chat Message Endpoint")
    print("=" * 50)
    
    chat_tests = [
        {
            "name": "Greeting",
            "payload": {"user_id": "user123", "message": "hello"}
        },
        {
            "name": "Service Inquiry",
            "payload": {"user_id": "user123", "message": "What services do you provide?"}
        },
        {
            "name": "Booking Request",
            "payload": {"user_id": "user123", "message": "I want a haircut"}
        },
        {
            "name": "Available Slots",
            "payload": {"user_id": "user123", "message": "Show me available slots for haircut"}
        },
        {
            "name": "Facial Service",
            "payload": {"user_id": "user123", "message": "What time do you have available for facial?"}
        },
        {
            "name": "Unknown Message",
            "payload": {"user_id": "user123", "message": "string"}
        }
    ]
    
    for test in chat_tests:
        print(f"\n📝 Test: {test['name']}")
        print(f"📤 Payload: {json.dumps(test['payload'], indent=2)}")
        
        try:
            response = requests.post("http://127.0.0.1:8000/chat/message", json=test['payload'])
            print(f"📥 Status: {response.status_code}")
            print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

def test_booking_endpoint():
    """Test the booking endpoint"""
    print("\n📅 Testing Booking Endpoint")
    print("=" * 50)
    
    booking_tests = [
        {
            "name": "Haircut Booking",
            "payload": {"user_id": "user123", "service": "haircut", "start_time": "2024-01-15T10:00:00"}
        },
        {
            "name": "Hair Wash Booking",
            "payload": {"user_id": "user123", "service": "hair_wash", "start_time": "2024-01-15T14:00:00"}
        },
        {
            "name": "Facial Booking",
            "payload": {"user_id": "user123", "service": "facial", "start_time": "2024-01-15T16:00:00"}
        },
        {
            "name": "Invalid Service",
            "payload": {"user_id": "user123", "service": "massage", "start_time": "2024-01-15T10:00:00"}
        }
    ]
    
    for test in booking_tests:
        print(f"\n📝 Test: {test['name']}")
        print(f"📤 Payload: {json.dumps(test['payload'], indent=2)}")
        
        try:
            response = requests.post("http://127.0.0.1:8000/booking", json=test['payload'])
            print(f"📥 Status: {response.status_code}")
            print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

def show_postman_json():
    """Show all JSON payloads for Postman"""
    print("\n📋 JSON Payloads for Postman")
    print("=" * 50)
    
    print("\n🎯 CHAT MESSAGE ENDPOINT")
    print("URL: POST http://127.0.0.1:8000/chat/message")
    print("Headers: Content-Type: application/json")
    
    chat_payloads = [
        {
            "name": "1. Greeting",
            "payload": {"user_id": "user123", "message": "hello"}
        },
        {
            "name": "2. Service Inquiry", 
            "payload": {"user_id": "user123", "message": "What services do you provide?"}
        },
        {
            "name": "3. Booking Request",
            "payload": {"user_id": "user123", "message": "I want a haircut"}
        },
        {
            "name": "4. Available Slots",
            "payload": {"user_id": "user123", "message": "Show me available slots for haircut"}
        },
        {
            "name": "5. Facial Service",
            "payload": {"user_id": "user123", "message": "What time do you have available for facial?"}
        },
        {
            "name": "6. Unknown Message",
            "payload": {"user_id": "user123", "message": "string"}
        }
    ]
    
    for test in chat_payloads:
        print(f"\n{test['name']}:")
        print(json.dumps(test['payload'], indent=2))
    
    print("\n🎯 BOOKING ENDPOINT")
    print("URL: POST http://127.0.0.1:8000/booking")
    print("Headers: Content-Type: application/json")
    
    booking_payloads = [
        {
            "name": "1. Haircut Booking",
            "payload": {"user_id": "user123", "service": "haircut", "start_time": "2024-01-15T10:00:00"}
        },
        {
            "name": "2. Hair Wash Booking",
            "payload": {"user_id": "user123", "service": "hair_wash", "start_time": "2024-01-15T14:00:00"}
        },
        {
            "name": "3. Facial Booking",
            "payload": {"user_id": "user123", "service": "facial", "start_time": "2024-01-15T16:00:00"}
        },
        {
            "name": "4. Invalid Service (Should fail)",
            "payload": {"user_id": "user123", "service": "massage", "start_time": "2024-01-15T10:00:00"}
        }
    ]
    
    for test in booking_payloads:
        print(f"\n{test['name']}:")
        print(json.dumps(test['payload'], indent=2))

if __name__ == "__main__":
    print("🧪 Salon Chatbot API Testing")
    print("=" * 60)
    
    # Show all JSON payloads for Postman
    show_postman_json()
    
    print("\n" + "=" * 60)
    print("🚀 Ready to test in Postman!")
    print("=" * 60) 