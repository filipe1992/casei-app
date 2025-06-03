from typing import Optional
from pydantic import BaseModel

class GuestBase(BaseModel):
    name: str
    phone: Optional[str] = None
    confirmed: bool = False
    whatsapp_invite_id: Optional[str] = None

class GuestCreate(GuestBase):
    pass

class GuestUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    confirmed: Optional[bool] = None
    whatsapp_invite_id: Optional[str] = None

class Guest(GuestBase):
    id: int
    hash_link: str
    user_id: int

    class Config:
        from_attributes = True 