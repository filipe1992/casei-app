from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.invitation import Invitation
from app.models.user import User
from app.schemas.invitation import GuestInvitationResponse, InvitationCreate, InvitationUpdate
from app.schemas.guest import Guest, GuestUpdate
from app.services.whatsapp import get_whatsapp_service
from app.crud import guest as guest_crud
import logging



async def get_invitation(db: AsyncSession, user_id: int) -> Optional[Invitation]:
    result = await db.execute(select(Invitation).where(Invitation.user_id == user_id))
    return result.scalar_one_or_none()

async def get_user_invitations(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Invitation]:
    result = await db.execute(
        select(Invitation)
        .where(Invitation.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_invitation(
    db: AsyncSession,
    invitation_in: InvitationCreate,
    user_id: int
) -> Invitation:
    db_invitation = Invitation(
        **invitation_in.model_dump(),
        user_id=user_id
    )
    db.add(db_invitation)
    await db.commit()
    await db.refresh(db_invitation)
    return db_invitation

async def update_invitation(
    db: AsyncSession,
    invitation: Invitation,
    invitation_in: InvitationUpdate
) -> Invitation:
    update_data = invitation_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invitation, field, value)
    
    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)
    return invitation

async def delete_invitation(
    db: AsyncSession,
    invitation_id: int,
    user_id: int
) -> Optional[Invitation]:
    result = await db.execute(
        select(Invitation).where(
            Invitation.id == invitation_id,
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
    )-> Optional[GuestInvitationResponse]:
    
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=hash_link)
    if not guest:
        logging.error(f"Convidado não encontrado: {hash_link}")
        raise HTTPException(status_code=404, detail=f"Convidado não encontrado: {hash_link}")
    
    invitation = await get_invitation(db=db, user_id=guest.user_id)
    if not invitation:
        logging.error(f"Convite não encontrado: {hash_link}")
        raise HTTPException(status_code=404, detail=f"Convite não encontrado: {hash_link}")
    
    # Retorna o convite com o nome do convidado usando o novo schema
    return GuestInvitationResponse(
        guest=guest,
        invitation=invitation
    ) 

async def send_invitation_by_whatsapp(
    db: AsyncSession,
    hash_link: str,
    user: User
    ):
    whatsapp = get_whatsapp_service()

    guest_invitation = await get_guest_invitation(db=db, hash_link=hash_link)
    if not guest_invitation:
        logging.error(f"Convite não encontrado: {hash_link}")
        raise HTTPException(status_code=404, detail=f"Convite não encontrado: {hash_link}")
    
    if user.id != guest_invitation.guest.user_id:
        logging.error(f"Você não tem permissão para enviar convite para este convidado")
        raise HTTPException(status_code=403, detail=f"Você não tem permissão para enviar convite para este convidado")
    
    guest_name = guest_invitation.guest.name
    invitation = guest_invitation.invitation.intro_text
    guest_link = f"https://weddingplanner.com.br/guest/{hash_link}"
    guest_phone = guest_invitation.guest.phone.replace("+", "")
    
    # Enviando uma mensagem simples
    try:
        result = await whatsapp.send_message(
            phone_number=guest_phone,  # Número sem o '+'
            message=f"Olá *{guest_name}!*\n\n *{user.full_name}* \n\n {invitation}\n\n Confirme sua presença em: {guest_link} \n\n\n\n\n> TESTANDO!!!!!!"
        )
        
        await guest_crud.update_guest(
            db=db, 
            guest= await guest_crud.get_guest_by_hash(db=db, hash_link=hash_link),
            guest_in=GuestUpdate(whatsapp_invite_id=result.get("id").get("_serialized"))
        )
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")
    

async def send_invitation_by_whatsapp_all_guests(
    db: AsyncSession,
    user: User
    ):
    whatsapp = get_whatsapp_service()

    guests = await guest_crud.get_guests_by_user(db=db, user_id=user.id)
    logging.info(f"Enviando convite para {len(guests)} convidados")
    for guest in guests:
        guest_phone = guest.phone.replace("+", "")
        guest_name = guest.name
        guest_link = f"https://weddingplanner.com.br/guest/{guest.hash_link}"
             
        # Enviando uma mensagem simples
        try:
            result = await whatsapp.send_message(
                phone_number=guest_phone,  # Número sem o '+'
                message=f"Olá *{guest_name}!*\n\n *Convite de casamento dos noivos {user.full_name} e {user.full_name}* \n\n Confira seu convite online e corta a nossa história: {guest_link} \n\n\n\n\n> TESTANDO!!!!!!"
            )
            
            await guest_crud.update_guest(
            db=db, 
                guest= await guest_crud.get_guest_by_hash(db=db, hash_link=guest.hash_link),
                guest_in=GuestUpdate(whatsapp_invite_id=result.get("id").get("_serialized"))
            )
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")
