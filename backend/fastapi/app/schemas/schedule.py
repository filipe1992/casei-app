from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date

# Schema para ScheduleItem
class ScheduleItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    time: datetime = Field(..., example="2025-05-29T14:30:00")  # Formato YYYY-MM-DD HH:MM:SS

class ScheduleItemCreate(ScheduleItemBase):
    pass

class ScheduleItemUpdate(ScheduleItemBase):
    pass

class ScheduleItemInDB(ScheduleItemBase):
    id: int
    schedule_id: int

    class Config:
        from_attributes = True

# Schema para Schedule
class ScheduleBase(BaseModel):
    title: str = "Cronograma do Evento"
    data_casamento: date = Field(..., example="2025-05-29")

class ScheduleCreate(ScheduleBase):
    items: List[ScheduleItemCreate]

class ScheduleUpdate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    user_id: int
    items: List[ScheduleItemInDB]

    class Config:
        from_attributes = True 