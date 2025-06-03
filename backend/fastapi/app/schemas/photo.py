from datetime import datetime
from pydantic import BaseModel

class PhotoBase(BaseModel):
    filename: str
    s3_key: str

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    filename: str | None = None
    s3_key: str | None = None

class Photo(PhotoBase):
    id: int
    upload_date: datetime
    hash_id: str
    user_id: int
    guest_id: int

    class Config:
        from_attributes = True

class PhotoResponse(Photo):
    guest_name: str
    url: str  # URL pré-assinada do S3 