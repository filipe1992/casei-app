from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Cronograma do Evento")
    data_casamento = Column(Date, nullable=False)
    # Relacionamento com o usuário (cada usuário só pode ter um cronograma)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="schedule")
    
    # Relacionamento com os itens do cronograma
    items = relationship("ScheduleItem", back_populates="schedule", cascade="all, delete-orphan")

class ScheduleItem(Base):
    __tablename__ = "schedule_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    time = Column(DateTime, nullable=False)  # Alterado de Time para DateTime
    
    # Relacionamento com o cronograma
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    schedule = relationship("Schedule", back_populates="items") 