from typing import Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.guest import Guest

def get_guests_by_confirmation(db: Session, user_id: int) -> Tuple[List[Guest], List[Guest]]:
    """
    Retorna duas listas: convidados confirmados e pendentes.
    """
    # Busca convidados confirmados
    confirmed = db.query(Guest).filter(
        Guest.user_id == user_id,
        Guest.confirmed == True  # noqa: E712
    ).order_by(Guest.name).all()
    
    # Busca convidados pendentes
    pending = db.query(Guest).filter(
        Guest.user_id == user_id,
        Guest.confirmed == False  # noqa: E712
    ).order_by(Guest.name).all()

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