from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    cor_principal = Column(String, nullable=True)
    cor_secundaria = Column(String, nullable=True)
    chave_pix = Column(String, nullable=True)
    data_casamento = Column(String, nullable=True)
    hora_casamento = Column(String, nullable=True)
    local_casamento = Column(String, nullable=True)
    cidade_casamento = Column(String, nullable=True)
    estado_casamento = Column(String, nullable=True)
    pais_casamento = Column(String, nullable=True)
    nome_noivo_1 = Column(String, nullable=True)
    nome_noivo_2 = Column(String, nullable=True)
    template_id = Column(String, nullable=True)

    # Relacionamento com o usuário (cada usuário só pode ter uma configuração)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="configuration")