from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    primary_color = Column(String, nullable=True)
    secondary_color = Column(String, nullable=True)
    pix_key = Column(String, nullable=True)
    pix_city = Column(String, nullable=True)
    wedding_date = Column(String, nullable=True)
    wedding_time = Column(String, nullable=True)
    wedding_location = Column(String, nullable=True)
    wedding_city = Column(String, nullable=True)
    wedding_state = Column(String, nullable=True)
    wedding_country = Column(String, nullable=True)
    spouse_name_1 = Column(String, nullable=True)
    spouse_name_2 = Column(String, nullable=True)
    template_id = Column(String, nullable=True)

    # Relacionamento com o usuário (one-to-one)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="configuration")