from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from app.db.base_class import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    intro_text = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    
    # Relacionamento com o usuário (one-to-one)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="invitation") 

    #relacionamento com o album de fotos
    photo_album_id = Column(Integer, ForeignKey("photo_albums.id"), nullable=True)
    photo_album = relationship("PhotoAlbum", back_populates="invitation")

    #relacionamento com a foto de capa
    cover_photo_id = Column(Integer, ForeignKey("photos.id"), nullable=True)
    cover_photo = relationship("Photo", back_populates="invitation")