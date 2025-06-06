from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ConfigurationBase(BaseModel):
    cor_principal: Optional[str] = None
    cor_secundaria: Optional[str] = None
    chave_pix: Optional[str] = None
    data_casamento: Optional[str] = None
    hora_casamento: Optional[str] = None
    local_casamento: Optional[str] = None
    cidade_casamento: Optional[str] = None
    estado_casamento: Optional[str] = None
    pais_casamento: Optional[str] = None
    nome_noivo_1: Optional[str] = None
    nome_noivo_2: Optional[str] = None
    template_id: Optional[str] = None

class ConfigurationCreate(ConfigurationBase):
    pass

class ConfigurationUpdate(BaseModel):
    cor_principal: Optional[str] = None
    cor_secundaria: Optional[str] = None
    chave_pix: Optional[str] = None
    data_casamento: Optional[str] = None
    hora_casamento: Optional[str] = None
    local_casamento: Optional[str] = None
    cidade_casamento: Optional[str] = None
    estado_casamento: Optional[str] = None
    pais_casamento: Optional[str] = None
    nome_noivo_1: Optional[str] = None
    nome_noivo_2: Optional[str] = None
    template_id: Optional[str] = None

class ConfigurationInDBBase(ConfigurationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Configuration(ConfigurationInDBBase):
    pass

# Schema para resposta pública (sem informações sensíveis)
class ConfigurationPublic(BaseModel):
    cor_principal: Optional[str] = None
    cor_secundaria: Optional[str] = None
    chave_pix: Optional[str] = None
    data_casamento: Optional[str] = None
    hora_casamento: Optional[str] = None
    local_casamento: Optional[str] = None
    cidade_casamento: Optional[str] = None
    estado_casamento: Optional[str] = None
    pais_casamento: Optional[str] = None
    nome_noivo_1: Optional[str] = None
    nome_noivo_2: Optional[str] = None
    template_id: Optional[str] = None

    class Config:
        from_attributes = True 