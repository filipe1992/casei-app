from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base_class import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    upload_date = Column(DateTime(timezone=False), default=datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    hash_id = Column(String, nullable=False, unique=True)
    
    # Relacionamento com o usuário (dono das fotos)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="photos", lazy="joined")
    
    # Relacionamento com o convidado que fez o upload
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    guest = relationship("Guest", back_populates="photos", lazy="joined") 