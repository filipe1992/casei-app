from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from app.db.base_class import Base

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)
    hash_link = Column(String, unique=True, index=True, nullable=False)
    whatsapp_invite_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relacionamento com o usuário (dono do evento)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="guests")

    # Relacionamento com os álbuns de fotos
    photo_albums = relationship("PhotoAlbum", back_populates="guest", cascade="all, delete-orphan")
    
    # Relacionamento com as tasks de desafios
    completed_challenge_tasks = relationship("CompletedChallengeTask", back_populates="guest", cascade="all, delete-orphan") 

    # Relacionamento com as compras da loja de presentes
    purchases = relationship("GiftShopPurchase", back_populates="guest", cascade="all, delete-orphan")