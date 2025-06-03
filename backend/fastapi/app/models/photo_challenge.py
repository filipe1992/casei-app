from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base_class import Base

class PhotoChallenge(Base):
    __tablename__ = "photo_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    
    # Relacionamento com o usuário (criador do desafio)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="photo_challenges")
    
    # Relacionamento com as tasks criadas para o challenge
    tasks = relationship("ChallengeTask", back_populates="challenge", cascade="all, delete-orphan")

class ChallengeTask(Base):
    __tablename__ = "challenge_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    
    # Relacionamento com o desafio
    challenge_id = Column(Integer, ForeignKey("photo_challenges.id"), nullable=False)
    challenge = relationship("PhotoChallenge", back_populates="tasks")

    # Relacionamento com as tarefas completadas
    completed_tasks = relationship("CompletedChallengeTask", back_populates="task", cascade="all, delete-orphan")

class CompletedChallengeTask(Base):
    __tablename__ = "completed_challenge_tasks"

    id = Column(Integer, primary_key=True, index=True)
    completed_at = Column(DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    
    # Relacionamento com a task do challenge
    task_id = Column(Integer, ForeignKey("challenge_tasks.id"), nullable=False)
    task = relationship("ChallengeTask", back_populates="completed_tasks")
    
    # Relacionamento com a foto
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)
    photo = relationship("Photo", backref="challenge_tasks")
    
    # Relacionamento com o convidado que completou a tarefa
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    guest = relationship("Guest", back_populates="completed_challenge_tasks")