from typing import Optional
from app.errors.base import create_validation_error, ErrorCode
from pydantic import BaseModel, HttpUrl, validator
import re
from app.schemas.guest import Guest

class InvitationBase(BaseModel):
    intro_text: str
    video_url: Optional[str] = None
    photo_album_url: Optional[str] = None
    background_image_url: str
    background_color: str = "#FFFFFF"

    @validator('background_color')
    def validate_hex_color(cls, v):
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Cor deve estar no formato hexadecimal (ex: #FF0000)",
                validation_errors=v
            )
        return v

    @validator('video_url')
    def validate_video_url(cls, v):
        if v is not None and not (v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtube') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/')
        ):
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="URL do vídeo deve ser do YouTube ou Vimeo",
                validation_errors=v
            )
        return v

class InvitationCreate(InvitationBase):
    pass

class InvitationUpdate(BaseModel):
    intro_text: Optional[str] = None
    video_url: Optional[str] = None
    photo_album_url: Optional[str] = None
    background_image_url: Optional[str] = None
    background_color: Optional[str] = None

    @validator('background_color')
    def validate_hex_color(cls, v):
        if v is not None and not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Cor deve estar no formato hexadecimal (ex: #FF0000)",
                validation_errors=v
            )
        return v

    @validator('video_url')
    def validate_video_url(cls, v):
        if v is not None and not (v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtube') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/')
        ):
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="URL do vídeo deve ser do YouTube ou Vimeo",
                validation_errors=v
            )
        return v

class Invitation(InvitationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class GuestInvitationResponse(BaseModel):
    guest: Guest    
    invitation: Invitation

    class Config:
        from_attributes = True 