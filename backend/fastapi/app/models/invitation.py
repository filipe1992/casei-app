from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    intro_text = Column(Text, nullable=False)  # Texto em formato rich text
    video_url = Column(String)  # Link do vídeo
    photo_album_url = Column(String)  # Link do álbum de fotos
    background_image_url = Column(String, nullable=False)  # URL da imagem de fundo
    background_color = Column(String, nullable=False, default="#FFFFFF")  # Cor em formato hex
    
    # Relacionamento com o usuário (cada usuário só pode ter um convite)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="invitation") 