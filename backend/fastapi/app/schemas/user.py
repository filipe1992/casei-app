from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.configuration import Configuration, ConfigurationPublic

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

# Schema que inclui dados do usuário e sua configuração
class UserWithConfiguration(User):
    configuration: Optional[Configuration] = None

    class Config:
        from_attributes = True