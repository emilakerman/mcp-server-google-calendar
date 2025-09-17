from pydantic import BaseModel

class CalendarEvent(BaseModel):
    summary: str 
    description: str
    start_time: str
    end_time: str
    location: str
    livestream_url: str

