from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from fastapi import UploadFile

# Schemas para Photo
class PhotoBase(BaseModel):
    filename: str
    s3_key: str

class PhotoCreate(BaseModel):
    user_id: int
    file: UploadFile  # Campo para receber o arquivo
    filename: str

class PhotoUpdate(BaseModel):
    filename: Optional[str] = None
    s3_key: Optional[str] = None
    photo_album_id: Optional[int] = None

class PhotoInDBBase(PhotoBase):
    id: int
    user_id: int
    upload_date: datetime
    photo_album_id: Optional[int] = None

    class Config:
        from_attributes = True

class Photo(PhotoInDBBase):
    pass

class PhotoResponse(Photo):
    url: str  # URL pré-assinada do S3

# Schemas para PhotoAlbum
class PhotoAlbumBase(BaseModel):
    name: str
    description: Optional[str] = None

class PhotoAlbumCreate(PhotoAlbumBase):
    user_id: int
    guest_id: Optional[int] = None  # Campo opcional para álbuns de convidados

class PhotoAlbumUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    guest_id: Optional[int] = None

class PhotoAlbumInDBBase(PhotoAlbumBase):
    id: int
    user_id: int
    guest_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PhotoAlbum(PhotoAlbumInDBBase):
    photos: List[Photo] = []

class PhotoAlbumResponse(PhotoAlbum):
    guest_name: Optional[str] = None  # Nome do convidado, se o álbum pertencer a um

# Schemas para PhotoGuest
class PhotoGuestBase(BaseModel):
    guest_id: int
    photo_id: int

class PhotoGuestCreate(PhotoGuestBase):
    pass

class PhotoGuestInDBBase(PhotoGuestBase):
    id: int

    class Config:
        from_attributes = True

class PhotoGuest(PhotoGuestInDBBase):
    pass

class PhotoGuestResponse(PhotoGuest):
    guest_name: str
    photo: PhotoResponse 