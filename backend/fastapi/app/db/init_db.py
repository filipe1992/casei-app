from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate

async def init_db(db: AsyncSession) -> None:
    """
    Inicializa o banco de dados com dados necessários
    """
    try:
        # Criar primeiro super usuário se não existir
        user = await get_user_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                full_name="Super Admin"
            )
            await create_user(db, user_in)
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        raise 