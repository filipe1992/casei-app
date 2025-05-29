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
    existing_invitation = invitation_crud.get_invitation(db=db, user_id=current_user.id)
    if existing_invitation:
        raise HTTPException(
            status_code=400,
            detail="Usuário já possui um convite"
        )
    invitation = invitation_crud.create_invitation(
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
    invitation = invitation_crud.get_invitation(db=db, user_id=current_user.id)
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
    invitation = invitation_crud.get_invitation(db=db, user_id=current_user.id)
    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )
    invitation = invitation_crud.update_invitation(
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
    invitation = invitation_crud.delete_invitation(db=db, user_id=current_user.id)
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
    guest = guest_crud.get_guest_by_hash(db=db, hash_link=hash_link)
    if not guest:
        raise HTTPException(
            status_code=404,
            detail="Convidado não encontrado"
        )
    
    invitation = invitation_crud.get_invitation(db=db, user_id=guest.user_id)
    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Convite não encontrado"
        )
    
    # Retorna o convite com o nome do convidado usando o novo schema
    return GuestInvitationResponse(
        guest_name=guest.name,
        invitation=invitation
    ) 