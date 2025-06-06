from typing import Optional, List

from app.errors.base import create_validation_error, ErrorCode
from pydantic import BaseModel, field_validator, model_validator, ValidationError
from typing_extensions import Annotated
from datetime import datetime
from app.schemas.invitation import PhotoBase

class TimelineItemBase(BaseModel):
    title: str
    text: Optional[str] = None
    video_url: Optional[str] = None
    photo_id: Optional[int] = None
    date: datetime

    @field_validator('video_url')
    @classmethod
    def validate_video_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            if not (
                v.startswith('https://www.youtube.com/') or 
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

    @model_validator(mode='after')
    def validate_content(self) -> 'TimelineItemBase':
        has_text = self.text is not None
        has_video = self.video_url is not None
        has_photo = self.photo_id is not None
        
        if not any([has_text, has_video, has_photo]):
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Pelo menos um dos campos (texto, vídeo ou foto) deve estar preenchido",
                validation_errors=self
            )
        if self.video_url and self.photo_id:
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Não pode ter vídeo e foto no mesmo item",
                validation_errors=self
            )
        return self

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TimelineItemCreate(TimelineItemBase):
    pass

class TimelineItemUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    video_url: Optional[str] = None
    photo_id: Optional[int] = None
    date: Optional[datetime] = None

    @field_validator('video_url')
    @classmethod
    def validate_video_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            # Se tiver uma URL de vídeo válida, limpa o photo_id
            if (
                v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtube') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/')
            ):
                # Limpa o photo_id se existir
                if 'photo_id' in info.data:
                    info.data['photo_id'] = None
                return v
            else:
                raise create_validation_error(
                    error_code=ErrorCode.INVALID_CONTENT,
                    message="URL do vídeo deve ser do YouTube ou Vimeo",
                    validation_errors=v
                )
        return v

    @field_validator('photo_id')
    @classmethod
    def validate_photo_id(cls, v: Optional[int], info) -> Optional[int]:
        if v is not None:
            # Se tiver uma foto, limpa a URL do vídeo
            if 'video_url' in info.data:
                info.data['video_url'] = None
        return v

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TimelineItem(TimelineItemBase):
    id: int
    timeline_id: int
    photo: Optional[PhotoBase] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TimelineBase(BaseModel):
    title: str = "Nossa história até aqui"

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TimelineCreate(TimelineBase):
    pass

class TimelineUpdate(BaseModel):
    title: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Timeline(TimelineBase):
    id: int
    user_id: int
    items: List[TimelineItem]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
