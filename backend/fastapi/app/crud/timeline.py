from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc

from app.models.timeline import Timeline, TimelineItem
from app.schemas.timeline import TimelineCreate, TimelineUpdate, TimelineItemCreate, TimelineItemUpdate

def get_timeline(db: Session, user_id: int, order_by_date: bool = False) -> Optional[Timeline]:
    """
    Retorna a timeline do usuário com seus itens.
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário
        order_by_date: Se True, ordena os itens por data (mais recente primeiro)
                      Se False, mantém a ordem padrão do banco
    """
    timeline = db.query(Timeline).filter(Timeline.user_id == user_id).first()
    
    if timeline and order_by_date:
        # Recarrega os itens ordenados por data
        timeline.items = (
            db.query(TimelineItem)
            .filter(TimelineItem.timeline_id == timeline.id)
            .order_by(desc(TimelineItem.date))
            .all()
        )
    
    return timeline

def create_timeline(db: Session, timeline_in: TimelineCreate, user_id: int) -> Timeline:
    db_timeline = Timeline(
        title=timeline_in.title,
        user_id=user_id
    )
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline

def update_timeline(
    db: Session,
    timeline: Timeline,
    timeline_in: TimelineUpdate
) -> Timeline:
    update_data = timeline_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timeline, field, value)
    
    db.add(timeline)
    db.commit()
    db.refresh(timeline)
    return timeline

def delete_timeline(db: Session, user_id: int) -> Optional[Timeline]:
    timeline = get_timeline(db=db, user_id=user_id)
    if timeline:
        db.delete(timeline)
        db.commit()
        return timeline
    return None

# Operações com itens da timeline

def get_timeline_item(db: Session, item_id: int) -> Optional[TimelineItem]:
    return db.query(TimelineItem).filter(TimelineItem.id == item_id).first()

def get_timeline_items(db: Session, timeline_id: int) -> List[TimelineItem]:
    return db.query(TimelineItem).filter(
        TimelineItem.timeline_id == timeline_id
    ).order_by(desc(TimelineItem.date)).all()

def create_timeline_item(
    db: Session,
    item_in: TimelineItemCreate,
    timeline_id: int
) -> TimelineItem:
    db_item = TimelineItem(
        **item_in.model_dump(),
        timeline_id=timeline_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_timeline_item(
    db: Session,
    item: TimelineItem,
    item_in: TimelineItemUpdate
) -> TimelineItem:
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_timeline_item(db: Session, item_id: int) -> Optional[TimelineItem]:
    item = get_timeline_item(db=db, item_id=item_id)
    if item:
        db.delete(item)
        db.commit()
        return item
    return None 