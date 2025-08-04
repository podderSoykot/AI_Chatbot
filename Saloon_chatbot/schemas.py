from pydantic import BaseModel
from datetime import datetime

class BookingRequest(BaseModel):
    message:str
    client_name:str="Guest"
class BookingResponse(BaseModel):
    response: str
    