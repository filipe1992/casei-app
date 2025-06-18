from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.auth.auth import get_password_hash, verify_password, create_access_token
from app.services.email import send_verification_email
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_with_configuration_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).options(selectinload(User.configuration)).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def send_new_account_email(email_to: str, name: str):
    # O token de confirmação pode ter uma vida útil curta
    expires_delta = timedelta(hours=1)
    token = create_access_token(data={"sub": email_to}, expires_delta=expires_delta)
    await send_verification_email(email_to=email_to, token=token, name=name)

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def deactivate_user(db: AsyncSession, username: str) -> Optional[User]:
    user = await get_user_by_email(db=db, email=username)
    if not user:
        return None
    
    # Não permite desativar superusuários
    if user.is_superuser:
        return None
    
    user.is_active = False
    await db.commit()
    db.refresh(user)
    return user 

async def confirm_email(db: AsyncSession, user: User) -> User:
    user.email_confirmed = True
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_by_id(db: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password" and value:
            setattr(user, "hashed_password", get_password_hash(value))
        elif value is not None:
            setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    if user.is_superuser:
        return None
    
    await db.delete(user)
    await db.commit()
    return user

