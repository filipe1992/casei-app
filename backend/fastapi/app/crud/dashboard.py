from typing import Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.guest import Guest

async def get_guests_by_confirmation(db: AsyncSession, user_id: int) -> Tuple[List[Guest], List[Guest]]:
    """
    Retorna duas listas: convidados confirmados e pendentes.
    """
    # Busca convidados confirmados
    confirmed = await db.execute(select(Guest).filter(
        Guest.user_id == user_id,
        Guest.confirmed == True  # noqa: E712
    ).order_by(Guest.name))
    confirmed = confirmed.scalars().all()
    
    # Busca convidados pendentes
    pending = await db.execute(select(Guest).filter(
        Guest.user_id == user_id,
        Guest.confirmed == False  # noqa: E712
    ).order_by(Guest.name))
    pending = pending.scalars().all()

    confirmed_count = len(confirmed)
    pending_count = len(pending)
    total = confirmed_count + pending_count

    confirmation_rate = (confirmed_count / total) * 100 if total > 0 else 0.0

    return {
        "confirmed": confirmed,
        "pending": pending,
        "confirmed_count": confirmed_count,
        "pending_count": pending_count,
        "total": total,
        "confirmation_rate": round(confirmation_rate, 2)
    }