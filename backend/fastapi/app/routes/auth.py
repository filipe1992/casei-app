from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import (
    create_access_token,
    get_current_user,
    get_current_active_superuser,
    update_access_token,
    get_password_hash,
    verify_password,
)
from app.core.config import settings
from app.crud import user as user_crud
from app.db.session import get_db
from app.schemas.user import User, UserCreate, ResetPassword, ResetPasswordLoggedUser
from app.services.email import send_password_reset_email

router = APIRouter()

@router.post("/login/access-token", response_model=dict[str, str])
async def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate_user(db, form_data.username, form_data.password)
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
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Create new user.
    """
    user = await user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Um usuário com este email já existe no sistema.",
        )
    user = await user_crud.create_user(db, user_in)
    
    # Adiciona a tarefa de envio de e-mail em segundo plano
    background_tasks.add_task(user_crud.send_new_account_email, email_to=user.email, name=user.full_name)

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
    user = await user_crud.deactivate_user(db=db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado ou é um superusuário que não pode ser desativado"
        )
    return user 

@router.post("/refresh-token", response_model=dict[str, str])
async def refresh_token(
    new_token: str = Depends(update_access_token)
) -> Any:
    """
    Refresh token.
    """
    return {
        "access_token": new_token,
        "token_type": "bearer",
    }

@router.get("/confirm-email/{token}")
async def confirm_email_route(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Confirm user email.
    """
    user = await get_current_user(db, token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de confirmação inválido ou expirado."
        )
    
    if user.email_confirmed:
        return {"message": "E-mail já confirmado."}

    await user_crud.confirm_email(db, user)
    return {"message": "E-mail confirmado com sucesso!"}

@router.post("/password-recovery/{email}")
async def recover_password(email: str, db: Session = Depends(get_db)):
    """
    Password Recovery
    """
    user = await user_crud.get_user_by_email(db, email=email)

    if user:
        # O token de redefinição pode ter uma vida útil curta, por exemplo, 1 hora
        password_reset_token = create_access_token(
            data={"sub": user.email}, expires_delta=timedelta(hours=1)
        )
        await send_password_reset_email(
            email_to=user.email, token=password_reset_token, name=user.full_name
        )

    return {"message": "Se um usuário com este e-mail existir, um link para redefinição de senha será enviado."}

@router.post("/reset-password/")
async def reset_password(
    data: ResetPassword,
    db: Session = Depends(get_db)
):
    """
    Reset password
    """
    user = await get_current_user(db, data.token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de redefinição inválido ou expirado."
        )

    hashed_password = get_password_hash(data.new_password)
    user.hashed_password = hashed_password
    await db.commit()

    return {"message": "Senha atualizada com sucesso!"}

@router.post("/reset-password-logged-user/")
async def reset_password_logged_user(
    data: ResetPasswordLoggedUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Reset password for logged user
    """
    user = current_user

    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta."
        )   

    hashed_password = get_password_hash(data.new_password)
    user.hashed_password = hashed_password
    await db.commit()

    return {"message": "Senha atualizada com sucesso!"}