import requests
import json

def test_database_functionality():
    """Test the database functionality"""
    print("🗄️ Testing Database Functionality")
    print("=" * 60)
    
    # Test creating bookings
    print("\n📅 Creating Bookings")
    print("=" * 50)
    
    booking_tests = [
        {
            "name": "1. Haircut Booking - User1",
            "payload": {"user_id": "user1", "service": "haircut", "start_time": "2024-01-15T10:00:00"}
        },
        {
            "name": "2. Hair Wash Booking - User2",
            "payload": {"user_id": "user2", "service": "hair_wash", "start_time": "2024-01-15T14:00:00"}
        },
        {
            "name": "3. Facial Booking - User1",
            "payload": {"user_id": "user1", "service": "facial", "start_time": "2024-01-16T16:00:00"}
        },
        {
            "name": "4. Haircut Booking - User3",
            "payload": {"user_id": "user3", "service": "haircut", "start_time": "2024-01-17T11:00:00"}
        }
    ]
    
    for test in booking_tests:
        print(f"\n📝 {test['name']}")
        print(f"📤 Request: {json.dumps(test['payload'], indent=2)}")
        
        try:
            response = requests.post("http://127.0.0.1:8000/booking", json=test['payload'])
            print(f"📥 Status: {response.status_code}")
            print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
    
    # Test getting all bookings
    print("\n📋 Getting All Bookings")
    print("=" * 50)
    
    try:
        response = requests.get("http://127.0.0.1:8000/bookings")
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test getting user-specific bookings
    print("\n👤 Getting User Bookings")
    print("=" * 50)
    
    user_tests = ["user1", "user2", "user3"]
    
    for user_id in user_tests:
        print(f"\n📝 Bookings for {user_id}:")
        try:
            response = requests.get(f"http://127.0.0.1:8000/bookings/{user_id}")
            print(f"📥 Status: {response.status_code}")
            print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_database_functionality()
    print("\n✅ Database Testing Complete!") 