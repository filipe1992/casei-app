from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.configuration import Configuration
from app.schemas.configuration import ConfigurationCreate, ConfigurationUpdate

async def create_configuration(db: AsyncSession, config_in: ConfigurationCreate, user_id: int) -> Configuration:
    """
    Cria uma nova configuração para o usuário.
    Cada usuário só pode ter uma configuração.
    """
    db_config = Configuration(
        cor_principal=config_in.cor_principal,
        cor_secundaria=config_in.cor_secundaria,
        chave_pix=config_in.chave_pix,
        data_casamento=config_in.data_casamento,
        hora_casamento=config_in.hora_casamento,
        local_casamento=config_in.local_casamento,
        cidade_casamento=config_in.cidade_casamento,
        estado_casamento=config_in.estado_casamento,
        pais_casamento=config_in.pais_casamento,
        nome_noivo_1=config_in.nome_noivo_1,
        nome_noivo_2=config_in.nome_noivo_2,
        user_id=user_id
    )
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    return db_config

async def get_configuration(db: AsyncSession, config_id: int) -> Optional[Configuration]:
    """
    Busca uma configuração pelo ID
    """
    result = await db.execute(select(Configuration).where(Configuration.id == config_id))
    return result.scalar_one_or_none()

async def get_user_configuration(db: AsyncSession, user_id: int) -> Optional[Configuration]:
    """
    Busca a configuração de um usuário específico
    """
    result = await db.execute(select(Configuration).where(Configuration.user_id == user_id))
    return result.scalar_one_or_none()

async def update_configuration(
    db: AsyncSession, 
    config_id: int, 
    config_in: ConfigurationUpdate
) -> Optional[Configuration]:
    """
    Atualiza uma configuração existente
    """
    db_config = await get_configuration(db, config_id)
    if not db_config:
        return None
    
    # Atualiza apenas os campos que foram fornecidos
    update_data = config_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_config, field, value)
    
    await db.commit()
    await db.refresh(db_config)
    return db_config

async def delete_configuration(db: AsyncSession, config_id: int) -> Optional[Configuration]:
    """
    Remove uma configuração
    """
    db_config = await get_configuration(db, config_id)
    if not db_config:
        return None
    
    await db.delete(db_config)
    await db.commit()
    return db_config

async def update_or_create_user_configuration(
    db: AsyncSession,
    user_id: int,
    config_in: ConfigurationUpdate
) -> Configuration:
    """
    Atualiza a configuração de um usuário se ela existir, ou cria uma nova se não existir
    """
    db_config = await get_user_configuration(db, user_id)
    
    if db_config:
        # Atualiza a configuração existente
        update_data = config_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_config, field, value)
    else:
        # Cria uma nova configuração
        config_data = config_in.model_dump(exclude_unset=True)
        db_config = Configuration(**config_data, user_id=user_id)
        db.add(db_config)
    
    await db.commit()
    await db.refresh(db_config)
    return db_config 