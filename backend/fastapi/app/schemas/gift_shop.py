from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator

from app.schemas.guest import Guest
from app.schemas.user import User
from app.schemas.invitation import PhotoBase

class GiftShopPurchaseBase(BaseModel):
    id: int
    created_at: datetime
    paid: bool
    paid_at: Optional[datetime] = None
    #guest: Guest

    class Config:
        from_attributes = True

class GiftProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., ge=0, le=99999999.99)
    image: Optional[str] = None
    photo_id: Optional[int] = None

    #validado para que o campo image seja uma url
    @validator('image')
    def validate_image(cls, v):
        if v and not v.startswith('http'):
            raise ValueError("A imagem deve ser uma URL válida")
        return v
    
    #validar para que não seja passado photo_id e image ao mesmo tempo
    @validator('photo_id', 'image')
    def validate_photo_id_and_image(cls, v, values):
        if v and values.get('image'):
            raise ValueError("Não é possível passar photo_id e image ao mesmo tempo")
        return v
    
class GiftProductCreate(GiftProductBase):
    pass

class GiftProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0, le=99999999.99)
    image: Optional[str] = None
    photo_id: Optional[int] = None

    #validado para que o campo image seja uma url
    @validator('image')
    def validate_image(cls, v):
        if v and not v.startswith('http'):
            raise ValueError("A imagem deve ser uma URL válida")
        return v
    
    #validar para que não seja passado photo_id e image ao mesmo tempo
    @validator('photo_id', 'image')
    def validate_photo_id_and_image(cls, v, values):
        if v and values.get('image'):
            raise ValueError("Não é possível passar photo_id e image ao mesmo tempo")
        return v

class GiftProduct(GiftProductBase):
    id: int
    shop_id: int
    photo: Optional[PhotoBase] = None
    
    class Config:
        from_attributes = True

class GiftProductWithPurchases(GiftProductBase):
    id: int
    shop_id: int
    photo: Optional[PhotoBase] = None
    purchases: Optional[List[GiftShopPurchaseBase]]
    
    class Config:
        from_attributes = True

class GiftShopBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class GiftShopCreate(GiftShopBase):
    pass

class GiftShopUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class GiftShop(GiftShopBase):
    id: int
    user_id: int
    products: List[GiftProduct] = []
    
    class Config:
        from_attributes = True

class GiftShopWithProducts(GiftShopBase):
    id: int
    user_id: int
    products: List[GiftProductWithPurchases] = []
    
    class Config:
        from_attributes = True

class GiftShopPurchase(BaseModel):
    pix_code: str
    product: GiftProductWithPurchases
    user: User
    guest: Guest

    class Config:
        from_attributes = True

class GiftShopPurchaseUpdate(BaseModel):
    paid: bool