import requests
import json

def test_chatbot():
    base_url = "http://127.0.0.1:8000/chat/message"
    
    # Test conversations
    conversations = [
        {"user_id": "user123", "message": "Hello"},
        {"user_id": "user123", "message": "What services do you provide?"},
        {"user_id": "user123", "message": "I want a haircut"},
        {"user_id": "user123", "message": "Show me available slots for haircut"},
        {"user_id": "user123", "message": "I want to book a haircut tomorrow at 2 PM"},
        {"user_id": "user123", "message": "What time do you have available for facial?"}
    ]
    
    print("🤖 Salon Chatbot Demo\n" + "="*50)
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n👤 User: {conv['message']}")
        
        try:
            response = requests.post(base_url, json=conv)
            if response.status_code == 200:
                reply = response.json()['reply']
                print(f"🤖 Bot: {reply}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_chatbot() 