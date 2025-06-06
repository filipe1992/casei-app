from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import configuration as configuration_crud
from app.schemas.configuration import (
    Configuration,
    ConfigurationCreate,
    ConfigurationUpdate,
    ConfigurationPublic
)
from app.models.user import User
from app.auth.auth import get_db, get_current_user

router = APIRouter()

@router.post("/configuration/", response_model=Configuration)
async def create_configuration(
    config_in: ConfigurationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Cria uma nova configuração para o usuário.
    """

    # Verifica se o usuário já tem uma configuração
    existing_config = await configuration_crud.get_user_configuration(db=db, user_id=current_user.id)
    if existing_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já possui uma configuração"
        )
    
    return await configuration_crud.create_configuration(db=db, config_in=config_in, user_id=current_user.id)

@router.get("/configuration/me", response_model=Configuration)
async def read_my_configuration(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recupera a configuração do usuário logado
    """
    config = await configuration_crud.get_user_configuration(db=db, user_id=current_user.id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuração não encontrada"
        )
    return config

@router.get("/configuration/{user_id}", response_model=ConfigurationPublic)
async def read_user_configuration(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Recupera a configuração pública de um usuário específico
    """
    config = await configuration_crud.get_user_configuration(db=db, user_id=user_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuração não encontrada"
        )
    return config

@router.put("/configuration/me", response_model=Configuration)
async def update_my_configuration(
    config_in: ConfigurationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualiza a configuração do usuário logado.
    Se não existir, cria uma nova.
    """
    return await configuration_crud.update_or_create_user_configuration(
        db=db,
        user_id=current_user.id,
        config_in=config_in
    )

@router.delete("/configuration/me", response_model=Configuration)
async def delete_my_configuration(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remove a configuração do usuário logado
    """
    config = await configuration_crud.get_user_configuration(db=db, user_id=current_user.id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuração não encontrada"
        )
    return await configuration_crud.delete_configuration(db=db, config_id=config.id)

