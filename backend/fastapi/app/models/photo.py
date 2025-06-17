from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.db.base_class import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    upload_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relacionamento com o usuário (dono das fotos)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="photos", lazy="joined")

    # Relacionamento com o álbum de fotos
    photo_album_id = Column(Integer, ForeignKey("photo_albums.id"), nullable=True)
    photo_album = relationship("PhotoAlbum", back_populates="photos", lazy="joined")

    # Relacionamento com o convite (foto de capa)
    invitation = relationship("Invitation", back_populates="cover_photo", uselist=False)

    # Relacionamento com os itens da timeline
    timeline_items = relationship("TimelineItem", back_populates="photo", lazy="joined")

    # Relacionamento com produtos da loja de presentes
    gift_products = relationship("GiftProduct", back_populates="photo", lazy="joined")
    
    
class PhotoAlbum(Base):
    __tablename__ = "photo_albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relacionamento com o usuário (dono do álbum)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="photo_albums", lazy="joined")

    # Relacionamento com o convidado (se o álbum é de um convidado)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=True)
    guest = relationship("Guest", back_populates="photo_albums", lazy="joined")

    # Relacionamento com as fotos do álbum
    photos = relationship("Photo", back_populates="photo_album", lazy="joined")

    # Relacionamento com o convite
    invitation = relationship("Invitation", back_populates="photo_album", uselist=False)
