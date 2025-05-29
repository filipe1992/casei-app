from sqlalchemy.orm import Session

from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.core.config import settings

def init_db(db: Session) -> None:
    # Verifica se já existe um superusuário
    user = get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name="Admin"
        )
        create_user(db, user_in) 