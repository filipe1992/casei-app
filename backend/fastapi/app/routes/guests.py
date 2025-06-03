import logging
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import guest as guest_crud
from app.schemas.guest import Guest, GuestCreate, GuestUpdate
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Guest)
async def create_guest(
    guest_in: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar novo convidado.
    """
    guest = await guest_crud.create_guest(db=db, guest_in=guest_in, user_id=current_user.id)
    return guest

@router.get("/me", response_model=List[Guest])
async def read_user_guests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar convidados do usuário atual.
    """
    guests = await guest_crud.get_guests_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return guests

@router.get("/{guest_id}", response_model=Guest)
async def read_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar um convidado específico.
    """
    guest = await guest_crud.get_guest(db=db, guest_id=guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    if guest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este convidado")
    return guest

@router.put("/{guest_id}", response_model=Guest)
async def update_guest(
    guest_id: int,
    guest_in: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um convidado.
    """
    guest = await guest_crud.get_guest(db=db, guest_id=guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    if guest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este convidado")
    guest = await guest_crud.update_guest(db=db, guest=guest, guest_in=guest_in)
    return guest

@router.delete("/{guest_id}", response_model=Guest)
async def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um convidado.
    """
    guest = await guest_crud.delete_guest(db=db, guest_id=guest_id, user_id=current_user.id)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    return guest

@router.post("/confirm/{hash_link}", response_model=Guest)
async def confirm_guest(
    hash_link: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Confirmar presença do convidado usando o hash_link.
    Esta rota é pública e não requer autenticação.
    """
    guest = await guest_crud.confirm_guest_presence(db=db, hash_link=hash_link)
    if not guest:
        raise HTTPException(status_code=404, detail="Link de confirmação inválido")
    return guest

@router.post("/send_invitation_all_guests_not_confirmed")
async def send_invitation_all_guests_not_confirmed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Enviar o convite por WhatsApp para todos os convidados não confirmados.
    """
    try:
        await guest_crud.send_invitation_by_whatsapp_all_guests_not_confirmed(db=db, user=current_user)
        return {"message": "Convite enviado para todos os convidados não confirmados"}
    except Exception as e:
        logging.error(f"Erro ao enviar convite para todos os convidados não confirmados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar convite para todos os convidados não confirmados: {str(e)}")
