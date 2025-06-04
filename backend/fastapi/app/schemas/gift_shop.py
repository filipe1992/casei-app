from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator

from app.schemas.guest import Guest
from app.schemas.user import User

class GiftShopBuyProductBase(BaseModel):
    id: int
    created_at: datetime
    payed: bool
    payed_at: Optional[datetime] = None
    #guest: Guest

    class Config:
        from_attributes = True

class GiftProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., ge=0, le=99999999.99)
    
class GiftProductCreate(GiftProductBase):
    image: str = Field(..., description="URL da imagem")
    
    @validator('image')
    def validate_image_url(cls, v):
        try:
            # Verifica se é uma URL válida
            if not v.startswith(('http://', 'https://')):
                raise ValueError('A URL deve começar com http:// ou https://')
            return v
        except Exception:
            raise ValueError('A URL da imagem deve ser válida')

class GiftProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0, le=99999999.99)
    image: Optional[str] = Field(None, description="URL da imagem")
    
    @validator('image')
    def validate_image_url(cls, v):
        if v is None:
            return v
        try:
            if not v.startswith(('http://', 'https://')):
                raise ValueError('A URL deve começar com http:// ou https://')
            return v
        except Exception:
            raise ValueError('A URL da imagem deve ser válida')

class GiftProduct(GiftProductBase):
    id: int
    shop_id: int
    image: str
    
    class Config:
        from_attributes = True

class GiftProductWithBuyProducts(GiftProductBase):
    id: int
    shop_id: int
    image: str
    buy_products: Optional[List[GiftShopBuyProductBase]]
    
    class Config:
        from_attributes = True

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

class GiftShopWithProducts(GiftShopBase):
    id: int
    user_id: int
    products: List[GiftProductWithBuyProducts] = []
    
    class Config:
        from_attributes = True

class GiftShopBuyProduct(BaseModel):
    codigo_pix: str
    product: GiftProductWithBuyProducts
    user: User
    guest: Guest

    class Config:
        from_attributes = True

class GiftShopBuyProductUpdate(BaseModel):
    payed: bool