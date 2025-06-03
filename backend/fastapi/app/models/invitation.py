from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    intro_text = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    photo_album_url = Column(String, nullable=True)
    background_image_url = Column(String, nullable=True)
    background_color = Column(String(7), nullable=True)  # Formato hex: #RRGGBB
    
    # Relacionamento com o usuário (one-to-one)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="invitation") 