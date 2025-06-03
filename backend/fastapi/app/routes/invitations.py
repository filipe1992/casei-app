import logging
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import invitation as invitation_crud
from app.crud import guest as guest_crud
from app.schemas.invitation import (
    Invitation,
    InvitationCreate,
    InvitationUpdate,
    GuestInvitationResponse
)
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Invitation)
async def create_invitation(
    invitation_in: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar novo convite.
    Cada usuário só pode ter um convite.
    """
    existing_invitation = await invitation_crud.get_invitation(db=db, user_id=current_user.id)
    if existing_invitation:
        raise HTTPException(
            status_code=400,
            detail="Usuário já possui um convite"
        )
    invitation = await invitation_crud.create_invitation(
        db=db, 
        invitation_in=invitation_in, 
        user_id=current_user.id
    )
    return invitation

@router.get("/me", response_model=Invitation)
async def read_invitation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar o convite do usuário atual.
    """
    invitation = await invitation_crud.get_invitation(db=db, user_id=current_user.id)
    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )
    return invitation

@router.put("/me", response_model=Invitation)
async def update_invitation(
    invitation_in: InvitationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar o convite do usuário atual.
    """
    invitation = await invitation_crud.get_invitation(db=db, user_id=current_user.id)
    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )
    invitation = await invitation_crud.update_invitation(
        db=db,
        invitation=invitation,
        invitation_in=invitation_in
    )
    return invitation

@router.delete("/me", response_model=Invitation)
async def delete_invitation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar o convite do usuário atual.
    """
    invitation = await invitation_crud.delete_invitation(db=db, user_id=current_user.id)
    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )
    return invitation

@router.get("/guest/{hash_link}", response_model=GuestInvitationResponse)
async def get_guest_invitation(
    hash_link: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Recuperar o convite personalizado para um convidado específico.
    Esta é uma rota pública que não requer autenticação.
    """

    return await invitation_crud.get_guest_invitation(db=db, hash_link=hash_link) 

@router.post("/guest/{hash_link}/send_invitation")
async def send_invitation(
    hash_link: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Enviar o convite por WhatsApp para um convidado específico.
    """
    try:
        await invitation_crud.send_invitation_by_whatsapp(db=db, hash_link=hash_link, user=current_user)
        return {"message": "Convite enviado para o convidado"}
    except Exception as e:
        logging.error(f"Erro ao enviar convite para o convidado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar convite para o convidado: {str(e)}")

@router.post("/send_invitation_all_guests")
async def send_invitation_all_guests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Enviar o convite por WhatsApp para todos os convidados.
    """
    try:
        await invitation_crud.send_invitation_by_whatsapp_all_guests(db=db, user=current_user)
        return {"message": "Convite enviado para todos os convidados"}
    except Exception as e:
        logging.error(f"Erro ao enviar convite para todos os convidados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar convite para todos os convidados: {str(e)}")