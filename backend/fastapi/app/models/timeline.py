from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Nossa história até aqui")
    
    # Relacionamento com o usuário (cada usuário só pode ter uma timeline)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="timeline")
    
    # Relacionamento com os itens da timeline
    items = relationship("TimelineItem", back_populates="timeline", cascade="all, delete-orphan")

class TimelineItem(Base):
    __tablename__ = "timeline_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(Text)
    video_url = Column(String)
    date = Column(DateTime, nullable=False)  # Nova coluna para data
    
    # Relacionamento com a timeline
    timeline_id = Column(Integer, ForeignKey("timelines.id"), nullable=False)
    timeline = relationship("Timeline", back_populates="items") 

    # relacionamento com a foto
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=True)
    photo = relationship("Photo", back_populates="timeline_items", uselist=False)