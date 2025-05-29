from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import dashboard as dashboard_crud
from app.schemas.dashboard import DashboardResponse, GuestMetrics
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user

router = APIRouter()

@router.get(
    "/",
    response_model=DashboardResponse,
    responses={
        200: {"description": "Dados do dashboard recuperados com sucesso"},
        500: {"description": "Erro do sistema"}
    }
)
async def read_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retorna os dados do dashboard para o usuário atual.
    
    Inclui:
    - Métricas gerais dos convidados (total, confirmados, pendentes, taxa de confirmação)
    - Lista de convidados confirmados
    - Lista de convidados pendentes
    """
    
    # Obtém as listas de convidados
    result = dashboard_crud.get_guests_by_confirmation(
        db=db, 
        user_id=current_user.id
    )
    
    return DashboardResponse(
        metrics= GuestMetrics(
            total_guests=result["total"],
            confirmed_count=result["confirmed_count"],
            pending_count=result["pending_count"],
            confirmation_rate=result["confirmation_rate"]
        ),
        confirmed_guests=result["confirmed"],
        pending_guests=result["pending"]
    ) 