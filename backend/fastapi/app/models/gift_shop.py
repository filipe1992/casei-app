from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, LargeBinary
from sqlalchemy.orm import relationship
from app.models.user import Base

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
    image = Column(LargeBinary, nullable=False)  # Armazena a imagem diretamente no banco
    
    # Relacionamento com a loja
    shop_id = Column(Integer, ForeignKey("gift_shops.id"), nullable=False)
    shop = relationship("GiftShop", back_populates="products") 