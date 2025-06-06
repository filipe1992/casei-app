from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ConfigurationBase(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    pix_key: Optional[str] = None
    pix_city: Optional[str] = None
    wedding_date: Optional[str] = None
    wedding_time: Optional[str] = None
    wedding_location: Optional[str] = None
    wedding_city: Optional[str] = None
    wedding_state: Optional[str] = None
    wedding_country: Optional[str] = None
    spouse_name_1: Optional[str] = None
    spouse_name_2: Optional[str] = None
    template_id: Optional[str] = None

class ConfigurationCreate(ConfigurationBase):
    pass

class ConfigurationUpdate(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    pix_key: Optional[str] = None
    pix_city: Optional[str] = None
    wedding_date: Optional[str] = None
    wedding_time: Optional[str] = None
    wedding_location: Optional[str] = None
    wedding_city: Optional[str] = None
    wedding_state: Optional[str] = None
    wedding_country: Optional[str] = None
    spouse_name_1: Optional[str] = None
    spouse_name_2: Optional[str] = None
    template_id: Optional[str] = None

class ConfigurationInDBBase(ConfigurationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Configuration(ConfigurationInDBBase):
    pass

# Schema for public response (without sensitive information)
class ConfigurationPublic(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    pix_key: Optional[str] = None
    pix_city: Optional[str] = None
    wedding_date: Optional[str] = None
    wedding_time: Optional[str] = None
    wedding_location: Optional[str] = None
    wedding_city: Optional[str] = None
    wedding_state: Optional[str] = None
    wedding_country: Optional[str] = None
    spouse_name_1: Optional[str] = None
    spouse_name_2: Optional[str] = None
    template_id: Optional[str] = None

    class Config:
        from_attributes = True 