import requests
import json
import time

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_chat_endpoint():
    """Test the chat message endpoint"""
    print("🤖 CHAT MESSAGE ENDPOINT")
    print("URL: POST http://127.0.0.1:8000/chat/message")
    print("=" * 50)
    
    # Test cases for chat
    test_cases = [
        {
            "name": "1. Greeting",
            "data": {
                "user_id": "user123",
                "message": "Hello"
            }
        },
        {
            "name": "2. Service Inquiry",
            "data": {
                "user_id": "user123",
                "message": "What services do you provide?"
            }
        },
        {
            "name": "3. Booking Request",
            "data": {
                "user_id": "user123",
                "message": "I want a haircut"
            }
        },
        {
            "name": "4. Check Slots",
            "data": {
                "user_id": "user123",
                "message": "What times are available?"
            }
        },
        {
            "name": "5. Unknown Intent",
            "data": {
                "user_id": "user123",
                "message": "Random message"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 {test_case['name']}")
        print(f"📤 Request: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(f"{BASE_URL}/chat/message", json=test_case['data'])
            print(f"📥 Status: {response.status_code}")
            print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
        time.sleep(1)  # Small delay between requests

def test_booking_endpoint():
    """Test the booking endpoint"""
    print("\n\n📅 BOOKING ENDPOINT")
    print("URL: POST http://127.0.0.1:8000/booking")
    print("=" * 50)
    
    # Test cases for booking
    test_cases = [
        {
            "name": "1. Haircut Booking",
            "data": {
                "user_id": "user123",
                "service": "haircut",
                "start_time": "2024-01-15T10:00:00"
            }
        },
        {
            "name": "2. Hair Wash Booking",
            "data": {
                "user_id": "user456",
                "service": "hair_wash",
                "start_time": "2024-01-15T14:30:00"
            }
        },
        {
            "name": "3. Facial Booking",
            "data": {
                "user_id": "user789",
                "service": "facial",
                "start_time": "2024-01-16T11:00:00"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 {test_case['name']}")
        print(f"📤 Request: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(f"{BASE_URL}/booking", json=test_case['data'])
            print(f"📥 Status: {response.status_code}")
            print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
        time.sleep(1)  # Small delay between requests

def test_database_endpoints():
    """Test the database endpoints"""
    print("\n\n🗄️ DATABASE ENDPOINTS")
    print("=" * 50)
    
    # Test GET all bookings
    print("\n📝 1. Get All Bookings")
    print("📤 Request: GET http://127.0.0.1:8000/bookings")
    try:
        response = requests.get(f"{BASE_URL}/bookings")
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 50)
    
    # Test GET user bookings
    print("\n📝 2. Get User Bookings")
    print("📤 Request: GET http://127.0.0.1:8000/bookings/user123")
    try:
        response = requests.get(f"{BASE_URL}/bookings/user123")
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 50)
    
    # Test DELETE booking (assuming booking ID 1 exists)
    print("\n📝 3. Delete Booking")
    print("📤 Request: DELETE http://127.0.0.1:8000/bookings/1")
    try:
        response = requests.delete(f"{BASE_URL}/bookings/1")
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 50)

def main():
    """Run all tests"""
    print("🧪 Testing API Endpoints - Real Responses")
    print("=" * 60)
    print()
    
    # Test chat endpoint
    test_chat_endpoint()
    
    # Test booking endpoint
    test_booking_endpoint()
    
    # Test database endpoints
    test_database_endpoints()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main() 