from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from app.db.base_class import Base

# from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    email_confirmed = Column(Boolean, default=False, nullable=False)
    full_name = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # Relacionamento com os convidados
    guests = relationship("Guest", back_populates="user", cascade="all, delete-orphan")
    
    # Relacionamento com o convite (one-to-one)
    invitation = relationship("Invitation", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento com a timeline (one-to-one)
    timeline = relationship("Timeline", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento com a loja de presentes (one-to-one)
    gift_shop = relationship("GiftShop", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento com as fotos
    photos = relationship("Photo", back_populates="user", cascade="all, delete-orphan")

    # Relacionamento com os álbuns de fotos
    photo_albums = relationship("PhotoAlbum", back_populates="user", cascade="all, delete-orphan")
    
    # Relacionamento com os desafios de fotos
    photo_challenges = relationship("PhotoChallenge", back_populates="user", cascade="all, delete-orphan")
    
    # Relacionamento com o cronograma (one-to-one)
    schedule = relationship("Schedule", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Relacionamento com a configuração (one-to-one)
    configuration = relationship("Configuration", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Relacionamentos
    menus = relationship("Menu", back_populates="user", cascade="all, delete-orphan")


