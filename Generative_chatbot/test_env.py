import os
from dotenv import load_dotenv

def test_env_setup():
    """Test environment variable setup"""
    print("🔧 Testing Environment Variable Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY loaded successfully")
        print(f"📝 API Key (first 20 chars): {api_key[:20]}...")
    else:
        print("❌ OPENAI_API_KEY not found")
    
    # Check database path
    db_path = os.getenv("DATABASE_PATH", "salon_bookings.db")
    print(f"🗄️ Database path: {db_path}")
    
    print("\n✅ Environment setup test complete!")

if __name__ == "__main__":
    test_env_setup() 