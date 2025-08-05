# AI Salon Booking Chatbot

A FastAPI-based REST API for a salon booking chatbot that uses OpenAI GPT-4o-mini for natural language understanding and SQLite for persistent booking storage.

## Features

- 🤖 **AI-Powered Chat**: Uses OpenAI GPT-4o-mini for intent recognition and entity extraction
- 📅 **Booking Management**: Create, view, and cancel salon appointments
- 🗄️ **Persistent Database**: SQLite database for storing all booking information
- 🔐 **Secure Configuration**: Environment variables for API keys and sensitive data
- 🎯 **REST API**: Clean RESTful endpoints for easy integration

## Services Offered

- **Haircut** (60 minutes)
- **Hair Wash** (30 minutes)
- **Facial** (45 minutes)

## API Endpoints

### Chat Endpoints

- `POST /chat/message` - Send messages to the chatbot
- `POST /booking` - Create a new booking
- `GET /bookings` - Get all bookings
- `GET /bookings/{user_id}` - Get bookings for a specific user
- `DELETE /bookings/{booking_id}` - Cancel a booking

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd AI_Chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the `Generative_chatbot` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_PATH=salon_bookings.db
```

### 5. Run the Application

```bash
cd Generative_chatbot
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## Example Usage

### Chat with the Bot

```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Hello"
  }'
```

### Create a Booking

```bash
curl -X POST "http://localhost:8000/booking" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "service": "haircut",
    "start_time": "2024-01-15T10:00:00"
  }'
```

### Get All Bookings

```bash
curl -X GET "http://localhost:8000/bookings"
```

## Project Structure

```
AI_Chatbot/
├── Generative_chatbot/
│   ├── main.py              # FastAPI application
│   ├── model.py             # Database models
│   ├── .env                 # Environment variables
│   ├── salon_bookings.db    # SQLite database
│   └── test_*.py           # Test files
├── Saloon_chatbot/          # Alternative implementation
├── requirements.txt          # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## Testing

Run the test files to verify functionality:

```bash
cd Generative_chatbot
python test_env.py           # Test environment setup
python test_api_responses.py # Test API endpoints
python test_database.py      # Test database functionality
```

## Environment Variables

| Variable         | Description               | Default             |
| ---------------- | ------------------------- | ------------------- |
| `OPENAI_API_KEY` | Your OpenAI API key       | Required            |
| `DATABASE_PATH`  | SQLite database file path | `salon_bookings.db` |

## Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- API keys are loaded securely from environment variables

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **OpenAI**: Python client for OpenAI API
- **python-dotenv**: Environment variable management
- **SQLite**: Lightweight database
- **Pydantic**: Data validation

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.
