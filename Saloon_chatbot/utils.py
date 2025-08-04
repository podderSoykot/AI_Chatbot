from datetime import datetime,timedelta

def parse_time_from_message(message:str) -> datetime:
    if "3 pm" in message.lower():
        return datetime.now().replace(hour=15,munite=0,second=0,microsecond=0)
    return None

def suggest_alternative(start_time: datetime) -> datetime:
    return start_time + timedelta(hours=1)
