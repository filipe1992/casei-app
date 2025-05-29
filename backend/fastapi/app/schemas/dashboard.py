from typing import List
from pydantic import BaseModel
from app.schemas.guest import Guest

class GuestMetrics(BaseModel):
    total_guests: int
    confirmed_count: int
    pending_count: int
    confirmation_rate: float

class DashboardResponse(BaseModel):
    metrics: GuestMetrics
    confirmed_guests: List[Guest]
    pending_guests: List[Guest]

    class Config:
        from_attributes = True 