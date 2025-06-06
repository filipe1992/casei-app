from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)
    hash_link = Column(String, unique=True, index=True, nullable=False)
    whatsapp_invite_id = Column(String, nullable=True)
    
    # Relacionamento com o usuário (dono do evento)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="guests")

    # Relacionamento com os álbuns de fotos
    photo_albums = relationship("PhotoAlbum", back_populates="guest", cascade="all, delete-orphan")
    
    # Relacionamento com as tasks de desafios
    completed_challenge_tasks = relationship("CompletedChallengeTask", back_populates="guest", cascade="all, delete-orphan") 

    # Relacionamento com as compras da loja de presentes
    buy_products = relationship("GiftShopBuyProduct", back_populates="guest", cascade="all, delete-orphan")