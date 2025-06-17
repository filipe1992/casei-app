from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Text, Float, ForeignKey, Boolean, Numeric, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from app.db.base_class import Base


class GiftShop(Base):
    __tablename__ = "gift_shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relationship with user (one-to-one)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="gift_shop")
    
    # Relationship with products
    products = relationship("GiftProduct", back_populates="shop", cascade="all, delete-orphan")

class GiftProduct(Base):
    __tablename__ = "gift_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)  # Allows values up to 99999999.99
    image = Column(String, nullable=True)  # Image URL (legacy)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # Relationship with photo
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=True)
    photo = relationship("Photo", back_populates="gift_products", uselist=False)

    # Relationship with shop
    shop_id = Column(Integer, ForeignKey("gift_shops.id"), nullable=False)
    shop = relationship("GiftShop", back_populates="products") 

    # Relationship with purchases
    purchases = relationship("GiftShopPurchase", back_populates="product", cascade="all, delete-orphan")


class GiftShopPurchase(Base):
    __tablename__ = "gift_shop_purchases"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    paid = Column(Boolean, default=False)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationship with product
    product_id = Column(Integer, ForeignKey("gift_products.id"), nullable=False)
    product = relationship("GiftProduct", back_populates="purchases")
    
    # Relationship with guest
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    guest = relationship("Guest", back_populates="purchases")


