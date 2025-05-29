from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.crud import timeline as timeline_crud
from app.schemas.timeline import (
    Timeline,
    TimelineCreate,
    TimelineUpdate,
    TimelineItem,
    TimelineItemCreate,
    TimelineItemUpdate
)
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user
from app.errors.base import (
    ErrorCode,
    create_not_found_error,
    create_already_exists_error,
    create_validation_error,
    create_access_denied_error,
    SystemError
)

router = APIRouter()

@router.post(
    "/",
    response_model=Timeline,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Timeline criada com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def create_timeline(
    timeline_in: TimelineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar nova timeline.
    
    - Cada usuário só pode ter uma timeline
    - O título é opcional, tendo um valor padrão
    """
    try:
        existing_timeline = timeline_crud.get_timeline(db=db, user_id=current_user.id)
        if existing_timeline:
            raise create_already_exists_error(
                resource_type="Timeline",
                identifier=current_user.id
            )
        
        timeline = timeline_crud.create_timeline(
            db=db,
            timeline_in=timeline_in,
            user_id=current_user.id
        )
        return timeline
    except ValueError as e:
        raise create_validation_error(
            message="Erro de validação dos dados da timeline",
            validation_errors=e.errors()
        )

@router.get(
    "/me",
    response_model=Timeline,
    responses={
        200: {"description": "Timeline recuperada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        400: {"description": "Erro de negócio"},
        500: {"description": "Erro do sistema"}
    }
)
async def read_timeline(
    order_by_date: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar a timeline do usuário atual.
    
    Parâmetros:
    - **order_by_date**: Se True, retorna os itens ordenados por data (mais recente primeiro).
                        Se False, mantém a ordem padrão do banco.
    
    Retorna:
    - Timeline com seus itens, ordenados conforme solicitado
    - 404 se a timeline não existir
    """
    timeline = timeline_crud.get_timeline(
        db=db, 
        user_id=current_user.id,
        order_by_date=order_by_date
    )
    
    if not timeline:
        raise create_not_found_error(
            resource_type="Timeline",
            resource_id=current_user.id
        )
    
    return timeline

@router.put(
    "/me",
    response_model=Timeline,
    responses={
        200: {"description": "Timeline atualizada com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def update_timeline(
    timeline_in: TimelineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar a timeline do usuário atual.
    
    - Permite atualizar apenas o título da timeline
    """
    try:
        timeline = timeline_crud.get_timeline(db=db, user_id=current_user.id)
        if not timeline:
            raise create_not_found_error(
                resource_type="Timeline",
                resource_id=current_user.id
            )
        
        timeline = timeline_crud.update_timeline(
            db=db,
            timeline=timeline,
            timeline_in=timeline_in
        )
        return timeline
    except ValidationError as e:
        raise create_validation_error(
            message="Erro de validação dos dados da timeline",
            validation_errors=e.errors()
        )

@router.delete(
    "/me",
    response_model=Timeline,
    responses={
        200: {"description": "Timeline deletada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def delete_timeline(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar a timeline do usuário atual.
    
    - A operação também remove todos os itens associados
    """
    timeline = timeline_crud.delete_timeline(db=db, user_id=current_user.id)
    if not timeline:
        raise create_not_found_error(
            resource_type="Timeline",
            resource_id=current_user.id
        )
    return timeline

# Rotas para itens da timeline

@router.post(
    "/me/items",
    response_model=TimelineItem,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Item criado com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def create_timeline_item(
    item_in: TimelineItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar novo item na timeline do usuário atual.
    
    Regras de validação:
    - Título é obrigatório
    - Data é obrigatória
    - Pelo menos um dos campos deve estar preenchido: texto, vídeo ou imagem
    - Não pode ter vídeo e imagem simultaneamente
    - URLs de vídeo devem ser do YouTube ou Vimeo
    - URLs de imagem devem ser http/https
    """
    try:
        timeline = timeline_crud.get_timeline(db=db, user_id=current_user.id)
        if not timeline:
            raise create_not_found_error(   
                resource_type="Timeline",
                resource_id=current_user.id
            )
        
        item = timeline_crud.create_timeline_item(
            db=db,
            item_in=item_in,
            timeline_id=timeline.id
        )
        return item
    except ValidationError as e:
        raise create_validation_error(
            message="Erro de validação dos dados do item",
            validation_errors=e.errors()
        )

@router.put(
    "/me/items/{item_id}",
    response_model=TimelineItem,
    responses={
        200: {"description": "Item atualizado com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def update_timeline_item(
    item_id: int,
    item_in: TimelineItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um item específico da timeline do usuário atual.
    
    Regras de validação:
    - Todos os campos são opcionais na atualização
    - Se houver vídeo, não pode ter imagem e vice-versa
    - URLs de vídeo devem ser do YouTube ou Vimeo
    - URLs de imagem devem ser http/https
    """
    try:
        timeline = timeline_crud.get_timeline(db=db, user_id=current_user.id)
        if not timeline:
            raise create_not_found_error(
                resource_type="Timeline",
                resource_id=current_user.id
            )
        
        item = timeline_crud.get_timeline_item(db=db, item_id=item_id)
        if not item:
            raise create_not_found_error(
                resource_type="Item da timeline",
                resource_id=item_id
            )
        
        if item.timeline_id != timeline.id:
            raise create_access_denied_error(
                resource_type="Item da timeline",
                resource_id=item_id
            )
        
        item = timeline_crud.update_timeline_item(
            db=db,
            item=item,
            item_in=item_in
        )
        return item
    except ValidationError as e:
        raise create_validation_error(
            message="Erro de validação dos dados do item",
            validation_errors=e.errors()
        )

@router.delete(
    "/me/items/{item_id}",
    response_model=TimelineItem,
    responses={
        200: {"description": "Item deletado com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def delete_timeline_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um item específico da timeline do usuário atual.
    """
    timeline = timeline_crud.get_timeline(db=db, user_id=current_user.id)
    if not timeline:
        raise create_not_found_error(
            resource_type="Timeline",
            resource_id=current_user.id
        )
    
    item = timeline_crud.get_timeline_item(db=db, item_id=item_id)
    if not item:
        raise create_not_found_error(
            resource_type="Item da timeline",
            resource_id=item_id
        )
    
    if item.timeline_id != timeline.id:
        raise create_access_denied_error(
            resource_type="Item da timeline",
            resource_id=item_id
        )
    
    item = timeline_crud.delete_timeline_item(db=db, item_id=item_id)
    return item 