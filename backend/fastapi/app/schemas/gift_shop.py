from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, validator
import base64

class GiftProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., ge=0, le=99999999.99)
    
class GiftProductCreate(GiftProductBase):
    image: str = Field(..., description="Imagem em base64")
    
    @validator('image')
    def validate_image(cls, v):
        try:
            # Tenta decodificar a imagem base64
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError('A imagem deve estar em formato base64 válido')

class GiftProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0, le=99999999.99)
    image: Optional[str] = Field(None, description="Imagem em base64")
    
    @validator('image')
    def validate_image(cls, v):
        if v is None:
            return v
        try:
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError('A imagem deve estar em formato base64 válido')

class GiftProduct(GiftProductBase):
    id: int
    shop_id: int
    image: str  # Será convertida para base64 na serialização
    
    class Config:
        from_attributes = True
        
    @validator('image', pre=True)
    def convert_image_to_base64(cls, v):
        if isinstance(v, bytes):
            return base64.b64encode(v).decode('utf-8')
        return v

class GiftShopBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    pix_key: str = Field(..., min_length=1, max_length=255)

class GiftShopCreate(GiftShopBase):
    pass

class GiftShopUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    pix_key: Optional[str] = Field(None, min_length=1, max_length=255)

class GiftShop(GiftShopBase):
    id: int
    user_id: int
    products: List[GiftProduct] = []
    
    class Config:
        from_attributes = True 