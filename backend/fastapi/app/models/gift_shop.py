from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Text, Float, ForeignKey, Boolean, Numeric, LargeBinary
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class GiftShop(Base):
    __tablename__ = "gift_shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    pix_key = Column(String, nullable=False)
    
    # Relacionamento com o usuário (cada usuário só pode ter uma loja)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="gift_shop")
    
    # Relacionamento com os produtos
    products = relationship("GiftProduct", back_populates="shop", cascade="all, delete-orphan")

class GiftProduct(Base):
    __tablename__ = "gift_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)  # Permite valores até 99999999.99
    image = Column(String, nullable=False)  # URL da imagem
    
    # Relacionamento com a loja
    shop_id = Column(Integer, ForeignKey("gift_shops.id"), nullable=False)
    shop = relationship("GiftShop", back_populates="products") 

    buy_products = relationship("GiftShopBuyProduct", back_populates="product", cascade="all, delete-orphan")


class GiftShopBuyProduct(Base):
    __tablename__ = "gift_shop_buy_products"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    payed = Column(Boolean, default=False)
    payed_at = Column(DateTime, nullable=True)

    product_id = Column(Integer, ForeignKey("gift_products.id"), nullable=False)
    product = relationship("GiftProduct", back_populates="buy_products")
    
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    guest = relationship("Guest", back_populates="buy_products")
    


