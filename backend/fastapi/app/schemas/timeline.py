from typing import Optional, List

from app.errors.base import create_validation_error
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
            # Verifica se tem imagem junto com vídeo
            if info.data.get('image_url'):
                raise create_validation_error(
                    message="Não pode ter vídeo e imagem no mesmo item",
                    validation_errors=v
                )
            # Valida URLs de vídeo
            if not (
                v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/')
            ):
                raise create_validation_error(
                    message="URL do vídeo deve ser do YouTube ou Vimeo",
                    validation_errors=v
                )
        return v

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            # Verifica se tem imagem junto com vídeo
            if info.data.get('video_url'):
                raise create_validation_error(
                    message="Não pode ter vídeo e imagem no mesmo item",
                    validation_errors=v
                )
            # Valida URLs de imagem
            if not (
                v.startswith('https:') or 
                v.startswith('http:') 
            ):
                raise create_validation_error(
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
                message="Pelo menos um dos campos (texto, vídeo ou imagem) deve estar preenchido",
                validation_errors=self
            )
        if self.video_url and self.image_url:
            raise create_validation_error(
                message="Não pode ter vídeo e imagem no mesmo item",
                validation_errors=self
            )
        return self

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
            if info.data.get('image_url'):
                raise create_validation_error(
                    message="Não pode ter vídeo e imagem no mesmo item",
                    validation_errors=v
                )
            if not (
                v.startswith('https://www.youtube.com/') or 
                v.startswith('https://youtu.be/') or
                v.startswith('https://vimeo.com/')
            ):
                raise create_validation_error(
                    message="URL do vídeo deve ser do YouTube ou Vimeo",
                    validation_errors=v
                )
        return v

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: Optional[str], info) -> Optional[str]:
        if v is not None:
            if info.data.get('video_url'):
                raise create_validation_error(
                    message="Não pode ter vídeo e imagem no mesmo item",
                    validation_errors=v
                )
            if not (
                v.startswith('https:') or 
                v.startswith('http:') 
            ):
                raise ValidationError(
                    message="URL da imagem deve ser de um site externoa",
                    validation_errors=v
                )
                # raise create_validation_error(
                #     message="URL da imagem deve ser de um site externo",
                #     validation_errors=v
                # )
        return v

class TimelineItem(TimelineItemBase):
    id: int
    timeline_id: int

    class Config:
        from_attributes = True

class TimelineBase(BaseModel):
    title: str = "Nossa história até aqui"

class TimelineCreate(TimelineBase):
    pass

class TimelineUpdate(BaseModel):
    title: Optional[str] = None

class Timeline(TimelineBase):
    id: int
    user_id: int
    items: List[TimelineItem]

    class Config:
        from_attributes = True
