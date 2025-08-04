from sqlalchemy import Column,Integer,String,DateTime
from database import Base 


#SQLAlchemy Model for Bookings
class Booking(Base):
    __tablename__='bookings'
    id=Column(Integer,primary_key=True,index=True)
    client_name=Column(String,nullable=False)
    service=Column(String)
    start_time=Column(DateTime,nullable=False)
    end_time=Column(DateTime,nullable=False)
