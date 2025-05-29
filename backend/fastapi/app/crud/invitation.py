from typing import Optional
from sqlalchemy.orm import Session
from app.models.invitation import Invitation
from app.schemas.invitation import InvitationCreate, InvitationUpdate

def get_invitation(db: Session, user_id: int) -> Optional[Invitation]:
    return db.query(Invitation).filter(Invitation.user_id == user_id).first()

def create_invitation(db: Session, invitation_in: InvitationCreate, user_id: int) -> Invitation:
    db_invitation = Invitation(
        intro_text=invitation_in.intro_text,
        video_url=invitation_in.video_url,
        photo_album_url=invitation_in.photo_album_url,
        background_image_url=invitation_in.background_image_url,
        background_color=invitation_in.background_color,
        user_id=user_id
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation

def update_invitation(
    db: Session, 
    invitation: Invitation, 
    invitation_in: InvitationUpdate
) -> Invitation:
    update_data = invitation_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invitation, field, value)
    
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation

def delete_invitation(db: Session, user_id: int) -> Optional[Invitation]:
    invitation = get_invitation(db=db, user_id=user_id)
    if invitation:
        db.delete(invitation)
        db.commit()
        return invitation
    return None 