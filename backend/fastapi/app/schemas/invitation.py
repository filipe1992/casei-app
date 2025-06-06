from typing import Optional
from app.errors.base import create_validation_error, ErrorCode
from pydantic import BaseModel, validator  
from app.schemas.guest import Guest
from datetime import datetime

class PhotoBase(BaseModel):
    id: int
    filename: str
    s3_key: str
    upload_date: datetime

    class Config:
        from_attributes = True

class PhotoAlbumBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class InvitationBase(BaseModel):
    intro_text: Optional[str] = None
    video_url: Optional[str] = None
    photo_album_id: Optional[int] = None
    cover_photo_id: Optional[int] = None

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
    photo_album_id: Optional[int] = None
    cover_photo_id: Optional[int] = None

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