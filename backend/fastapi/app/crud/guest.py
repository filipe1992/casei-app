import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import hashlib
import uuid
import time

from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestStatistics, GuestUpdate
from app.services.whatsapp import get_whatsapp_service
from app.models.user import User

async def get_guest(db: AsyncSession, guest_id: int) -> Optional[Guest]:
    result = await db.execute(select(Guest).where(Guest.id == guest_id))
    return result.scalar_one_or_none()

async def get_guest_by_hash(db: AsyncSession, hash_link: str) -> Optional[Guest]:
    result = await db.execute(select(Guest).where(Guest.hash_link == hash_link))
    return result.scalar_one_or_none()

async def get_guests_by_user(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Guest]:
    result = await db.execute(
        select(Guest)
        .where(Guest.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(func.lower(Guest.name).asc())
    )
    return result.scalars().all()


async def get_statistics_about_guests(db: AsyncSession, user_id: int) -> GuestStatistics:
    result = await db.execute(
        select(Guest)
        .where(Guest.user_id == user_id)
    )
    guests = result.scalars().all()

    total_guests = len(guests)
    total_confirmed_guests = sum(1 for guest in guests if guest.confirmed)
    total_unconfirmed_guests = total_guests - total_confirmed_guests
    percentage_confirmed_guests = total_confirmed_guests / total_guests * 100

    return {
        "total_guests": int(total_guests),
        "total_confirmed_guests": int(total_confirmed_guests),
        "total_unconfirmed_guests": int(total_unconfirmed_guests),
        "percentage_confirmed_guests": float(percentage_confirmed_guests),
    }

async def get_unconfirmed_guests_by_user(
    db: AsyncSession,
    user_id: int,
) -> List[Guest]:
    result = await db.execute(
        select(Guest)
        .where(Guest.user_id == user_id)
        .where(Guest.confirmed == False)
    )
    return result.scalars().all()

async def create_guest(
    db: AsyncSession,
    guest_in: GuestCreate,
    user_id: int 
) -> Guest:
    # Cria um hash único baseado no nome do convidado e um UUID
    unique_string = f"{guest_in.name}-{uuid.uuid4()}"
    hash_link = hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    db_guest = Guest(
        name=guest_in.name,
        phone=guest_in.phone,
        confirmed=guest_in.confirmed,
        hash_link=hash_link,
        user_id=user_id
    )
    db.add(db_guest)
    await db.commit()
    await db.refresh(db_guest)
    return db_guest

async def update_guest(
    db: AsyncSession,
    guest_id: int,
    guest_in: GuestUpdate
) -> Guest:
    guest = await get_guest(db, guest_id)
    if not guest:
        return None
    
    update_data = guest_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guest, field, value)
    
    db.add(guest)
    await db.commit()
    await db.refresh(guest)
    return guest

async def delete_guest(
    db: AsyncSession,
    guest_id: int,
    user_id: int
) -> Optional[Guest]:
    result = await db.execute(
        select(Guest).where(
            Guest.id == guest_id,
            Guest.user_id == user_id
        )
    )
    guest = result.scalar_one_or_none()
    
    if guest:
        await db.delete(guest)
        await db.commit()
    
    return guest

async def confirm_guest_presence(db: AsyncSession, hash_link: str) -> Optional[Guest]:
    guest = await get_guest_by_hash(db, hash_link)
    if guest:
        guest.confirmed = True
        db.commit()
        db.refresh(guest)
        return guest
    return None 

async def send_invitation_by_whatsapp_all_guests_not_confirmed(db: AsyncSession, user: User) -> None:
    whatsapp = get_whatsapp_service()
    guests = await get_unconfirmed_guests_by_user(db, user.id)
    
    logging.info(f"Enviando convite para {len(guests)} convidados")
    for guest in guests:
        guest_phone = guest.phone.replace("+", "")
        guest_name = guest.name
        guest_link = f"https://weddingplanner.com.br/guest/{guest.hash_link}"
             
        # Enviando uma mensagem simples
        try:
            _ = await whatsapp.send_message(
                phone_number=guest_phone,  # Número sem o '+'
                message=f"Olá *{guest_name}!*\n\n *{user.full_name}* estão entrando em contato para que voce confirme sua presença no casamento.\n\n {guest_link} \n\n\n\n\n> TESTANDO!!!!!!",
                reply_to=guest.whatsapp_invite_id
            )
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")

async def send_reaction_to_all_guests_not_confirmed(db: AsyncSession, user: User) -> None:
    whatsapp = get_whatsapp_service()
    guests = await get_unconfirmed_guests_by_user(db, user.id)
    
    logging.info(f"Enviando convite para {len(guests)} convidados")
    for guest in guests:

        try:
            await whatsapp.send_reaction(
                message_id=guest.whatsapp_invite_id,
                reaction="🤔", # :thinking:
                session="default"
            )
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")
        time.sleep(1)
    logging.info(f"Reação enviada para todos os convidados não confirmados")

