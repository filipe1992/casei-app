from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import user as user_crud
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel
from app.auth.auth import get_db, get_current_user, get_current_active_superuser
from app.schemas.configuration import Configuration
from app.crud import configuration as configuration_crud

router = APIRouter()

@router.get("/", response_model=List[User])
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_superuser)
) -> Any:
    """
    Recupera todos os usuários.
    Apenas superusuários podem acessar esta rota.
    """
    users = await user_crud.get_users(db, skip, limit)
    return users

@router.post("/", response_model=User)
async def create_new_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(get_current_active_superuser)
) -> Any:
    """
    Cria um novo usuário.
    Apenas superusuários podem criar outros usuários.
    """
    user = await user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Um usuário com este email já existe no sistema."
        )
    user = await user_crud.create_user(db, user_in)
    return user

@router.get("/me", response_model=User)
async def read_user_me(
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    Recupera o usuário atual.
    """
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    Atualiza os dados do usuário atual.
    """
    user = await user_crud.update_user_by_id(db, current_user.id, user_in)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    
    return user

@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(get_current_active_superuser),
    db: Session = Depends(get_db)
) -> Any:
    """
    Recupera um usuário específico pelo ID.
    Apenas superusuários podem acessar esta rota.
    """
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_superuser)
) -> Any:
    """
    Atualiza um usuário específico.
    Apenas superusuários podem atualizar outros usuários.
    """    
    user = await user_crud.update_user_by_id(db, user_id, user_in)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    return user

@router.delete("/{user_id}", response_model=User)
async def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_active_superuser)
) -> Any:
    """
    Remove um usuário do sistema.
    Apenas superusuários podem remover usuários.
    Não é possível remover superusuários.
    """
    user = await user_crud.delete_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    return user 