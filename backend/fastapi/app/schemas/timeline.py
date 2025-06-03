from typing import Optional, List

from app.errors.base import create_validation_error, ErrorCode
from pydantic import BaseModel, field_validator, model_validator, ValidationError
from typing_extensions import Annotated
from datetime import datetime

class TimelineItemBase(BaseModel):
    title: str
    text: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    date: datetime

    @field_validator('video_url')
    @classmethod
    def validate_video_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            # Valida URLs de vídeo
            if not (
                v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtube') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/')
            ):
                raise create_validation_error(
                    error_code=ErrorCode.INVALID_CONTENT,
                    message="URL do vídeo deve ser do YouTube ou Vimeo++",
                    validation_errors=v
                )
        return v

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            # Valida URLs de imagem
            if not (
                v.startswith('https:') or 
                v.startswith('http:') 
            ):
                raise create_validation_error(
                    error_code=ErrorCode.INVALID_CONTENT,
                    message="URL da imagem deve ser de um site externo",
                    validation_errors=v
                )
        return v

    @model_validator(mode='after')
    def validate_content(self) -> 'TimelineItemBase':
        has_text = self.text is not None
        has_video = self.video_url is not None
        has_image = self.image_url is not None
        
        if not any([has_text, has_video, has_image]):
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Pelo menos um dos campos (texto, vídeo ou imagem) deve estar preenchido",
                validation_errors=self
            )
        if self.video_url and self.image_url:
            raise create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Não pode ter vídeo e imagem no mesmo item.....",
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
    image_url: Optional[str] = None
    date: Optional[datetime] = None

    @field_validator('video_url')
    @classmethod
    def validate_video_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            # Se tiver uma URL de vídeo válida, limpa a URL da imagem
            if ( 
                (v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtube') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/'))
            ):
                # Limpa a URL da imagem se existir
                if 'image_url' in info.data:
                    info.data['image_url'] = None
                return v
            else:
                raise create_validation_error(
                    error_code=ErrorCode.INVALID_CONTENT,
                    message="URL do vídeo deve ser do YouTube ou Vimeo",
                    validation_errors=v
                )
        return v

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            # Se tiver uma URL de imagem válida, limpa a URL do vídeo
            if v.startswith('https:') or v.startswith('http:'):
                # Limpa a URL do vídeo se existir
                if 'video_url' in info.data:
                    info.data['video_url'] = None
                return v
            else:
                raise create_validation_error(
                    error_code=ErrorCode.INVALID_CONTENT,
                    message="URL da imagem deve ser de um site externo",
                    validation_errors=v
                )
        return v

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TimelineItem(TimelineItemBase):
    id: int
    timeline_id: int

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
