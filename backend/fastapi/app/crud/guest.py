from typing import List, Optional
from sqlalchemy.orm import Session
import hashlib
import uuid

from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestUpdate

def create_guest(db: Session, guest_in: GuestCreate, user_id: int) -> Guest:
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
    db.commit()
    db.refresh(db_guest)
    return db_guest

def get_guest(db: Session, guest_id: int) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.id == guest_id).first()

def get_guest_by_hash(db: Session, hash_link: str) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.hash_link == hash_link).first()

def get_user_guests(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Guest]:
    return db.query(Guest).filter(Guest.user_id == user_id).offset(skip).limit(limit).all()

def update_guest(db: Session, guest: Guest, guest_in: GuestUpdate) -> Guest:
    update_data = guest_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guest, field, value)
    
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

def delete_guest(db: Session, guest_id: int, user_id: int) -> Optional[Guest]:
    guest = db.query(Guest).filter(
        Guest.id == guest_id,
        Guest.user_id == user_id
    ).first()
    
    if guest:
        db.delete(guest)
        db.commit()
        return guest
    
    return None

def confirm_guest_presence(db: Session, hash_link: str) -> Optional[Guest]:
    guest = get_guest_by_hash(db, hash_link)
    if guest:
        guest.confirmed = True
        db.commit()
        db.refresh(guest)
        return guest
    return None 