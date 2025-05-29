from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import (
    create_access_token,
    get_current_user,
    get_current_active_superuser
)
from app.core.config import settings
from app.crud.user import authenticate_user, create_user, get_user_by_email, deactivate_user
from app.db.session import get_db
from app.schemas.user import User, UserCreate

router = APIRouter()

@router.post("/login/access-token", response_model=dict[str, str])
async def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=User)
async def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Um usuário com este email já existe no sistema.",
        )
    user = create_user(db, user_in)
    return user

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.post("/test-superuser", response_model=User)
async def test_superuser(
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Test superuser access
    """
    return current_user

@router.post("/users/{username}/deactivate", response_model=User)
async def deactivate_user_route(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Desativa um usuário do sistema.
    Somente superusuários podem executar esta ação.
    Não é possível desativar superusuários.
    """
    user = deactivate_user(db=db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado ou é um superusuário que não pode ser desativado"
        )
    return user 