from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # Relacionamento com os convidados
    guests = relationship("Guest", back_populates="user", cascade="all, delete-orphan")
    
    # Relacionamento com o convite (one-to-one)
    invitation = relationship("Invitation", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento com a timeline (one-to-one)
    timeline = relationship("Timeline", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento com a loja de presentes (one-to-one)
    gift_shop = relationship("GiftShop", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relacionamento com os convites (many-to-many)
    invitations = relationship("Invitation", back_populates="user") 