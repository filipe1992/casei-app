from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.invitation import Invitation
from app.models.user import User
from app.schemas.invitation import GuestInvitationResponse, InvitationCreate, InvitationUpdate
from app.schemas.guest import Guest, GuestUpdate
from app.services.whatsapp import get_whatsapp_service
from app.crud import guest as guest_crud
import logging



async def get_invitation(db: AsyncSession, user_id: int) -> Optional[Invitation]:
    """
    Busca o convite de um usuário com suas relações (álbum de fotos e foto de capa).
    """
    result = await db.execute(
        select(Invitation)
        .where(Invitation.user_id == user_id)
        .options(
            joinedload(Invitation.photo_album),
            joinedload(Invitation.cover_photo)
        )
    )
    return result.unique().scalar_one_or_none()

async def get_user_invitations(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Invitation]:
    """
    Busca todos os convites de um usuário com suas relações.
    """
    result = await db.execute(
        select(Invitation)
        .where(Invitation.user_id == user_id)
        .options(
            joinedload(Invitation.photo_album),
            joinedload(Invitation.cover_photo)
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_invitation(
    db: AsyncSession,
    invitation_in: InvitationCreate,
    user_id: int
) -> Invitation:
    """
    Cria um novo convite para o usuário.
    """
    db_invitation = Invitation(
        **invitation_in.model_dump(),
        user_id=user_id
    )
    db.add(db_invitation)
    await db.commit()
    await db.refresh(db_invitation)
    
    # Recarrega o convite com suas relações
    return await get_invitation(db=db, user_id=user_id)

async def update_invitation(
    db: AsyncSession,
    invitation: Invitation,
    invitation_in: InvitationUpdate
) -> Invitation:
    """
    Atualiza um convite existente.
    """
    update_data = invitation_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invitation, field, value)
    
    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)
    
    # Recarrega o convite com suas relações
    return await get_invitation(db=db, user_id=invitation.user_id)

async def delete_invitation(
    db: AsyncSession,
    user_id: int
) -> Optional[Invitation]:
    """
    Remove um convite existente.
    """
    result = await db.execute(
        select(Invitation).where(
            Invitation.user_id == user_id
        )
    )
    invitation = result.scalar_one_or_none()
    
    if invitation:
        await db.delete(invitation)
        await db.commit()
    
    return invitation 

async def get_guest_invitation(
    db: AsyncSession,
    hash_link: str  
) -> Optional[GuestInvitationResponse]:
    """
    Busca o convite de um convidado pelo hash do link.
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=hash_link)
    if not guest:
        logging.error(f"Convidado não encontrado: {hash_link}")
        raise HTTPException(status_code=404, detail=f"Convidado não encontrado: {hash_link}")
    
    invitation = await get_invitation(db=db, user_id=guest.user_id)
    if not invitation:
        logging.error(f"Convite não encontrado: {hash_link}")
        raise HTTPException(status_code=404, detail=f"Convite não encontrado: {hash_link}")
    
    return GuestInvitationResponse(
        guest=guest,
        invitation=invitation
    ) 

async def send_invitation_by_whatsapp(
    db: AsyncSession,
    hash_link: str,
    user: User
) -> None:
    """
    Envia o convite por WhatsApp para um convidado específico.
    """
    whatsapp = get_whatsapp_service()

    guest_invitation = await get_guest_invitation(db=db, hash_link=hash_link)
    if not guest_invitation:
        logging.error(f"Convite não encontrado: {hash_link}")
        raise HTTPException(status_code=404, detail=f"Convite não encontrado: {hash_link}")
    
    if user.id != guest_invitation.guest.user_id:
        logging.error(f"Você não tem permissão para enviar convite para este convidado")
        raise HTTPException(status_code=403, detail=f"Você não tem permissão para enviar convite para este convidado")
    
    guest_name = guest_invitation.guest.name
    invitation_text = guest_invitation.invitation.intro_text or "Você está convidado(a) para o nosso casamento!"
    guest_link = f"https://weddingplanner.com.br/guest/{hash_link}"
    guest_phone = guest_invitation.guest.phone.replace("+", "")
    
    try:
        result = await whatsapp.send_message(
            phone_number=guest_phone,
            message=f"Olá *{guest_name}!*\n\n{invitation_text}\n\nConfira seu convite online e confirme sua presença em: {guest_link}"
        )
        
        await guest_crud.update_guest(
            db=db, 
            guest_id=guest_invitation.guest.id,
            guest_in=GuestUpdate(whatsapp_invite_id=result.get("id").get("_serialized"))
        )
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")

async def send_invitation_by_whatsapp_all_guests(
    db: AsyncSession,
    user: User
) -> None:
    """
    Envia o convite por WhatsApp para todos os convidados do usuário.
    """
    whatsapp = get_whatsapp_service()
    invitation = await get_invitation(db=db, user_id=user.id)
    
    if not invitation:
        logging.error(f"Convite não encontrado para o usuário: {user.id}")
        raise HTTPException(status_code=404, detail="Convite não encontrado")

    guests = await guest_crud.get_guests_by_user(db=db, user_id=user.id)
    logging.info(f"Enviando convite para {len(guests)} convidados")
    
    invitation_text = invitation.intro_text or "Você está convidado(a) para o nosso casamento!"
    
    for guest in guests:
        try:
            await send_invitation_by_whatsapp(db=db, hash_link=guest.hash_link, user=user)
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem para {guest.name}: {str(e)}")
            continue  # Continue enviando para outros convidados mesmo se houver erro
