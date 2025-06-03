from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy.orm import selectinload

from app.models.timeline import Timeline, TimelineItem
from app.schemas.timeline import TimelineCreate, TimelineUpdate, TimelineItemCreate, TimelineItemUpdate

async def get_timeline(db: AsyncSession, timeline_id: int) -> Optional[Timeline]:
    result = await db.execute(select(Timeline).where(Timeline.id == timeline_id))
    return result.scalar_one_or_none()

async def get_user_timeline(db: AsyncSession, user_id: int) -> Optional[Timeline]:
    stmt = (
        select(Timeline)
        .options(selectinload(Timeline.items))  # CARREGA OS ITENS ANTECIPADAMENTE
        .where(Timeline.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
    

async def create_timeline(
    db: AsyncSession,
    timeline_in: TimelineCreate,
    user_id: int
) -> Timeline:
    db_timeline = Timeline(
        title=timeline_in.title,
        user_id=user_id
    )
    db.add(db_timeline)
    await db.commit()
    await db.refresh(db_timeline)
    return await get_user_timeline(db=db, user_id=user_id)

async def update_timeline(
    db: AsyncSession,
    timeline: Timeline,
    timeline_in: TimelineUpdate
) -> Timeline:
    update_data = timeline_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timeline, field, value)
    
    db.add(timeline)
    await db.commit()
    await db.refresh(timeline)
    return timeline

async def delete_timeline(
    db: AsyncSession,
    user_id: int
) -> Optional[Timeline]:
    result = await db.execute(
        select(Timeline).where(
            Timeline.user_id == user_id
        )
    )
    timeline = result.scalar_one_or_none()
    
    if timeline:
        await db.delete(timeline)
        await db.commit()
    
    return timeline

# Operações com itens da timeline

async def get_timeline_item(db: AsyncSession, item_id: int) -> Optional[TimelineItem]:
    result = await db.execute(select(TimelineItem).where(TimelineItem.id == item_id))
    return result.scalar_one_or_none()

async def get_timeline_items(db: AsyncSession, timeline_id: int) -> List[TimelineItem]:
    result = await db.execute(select(TimelineItem).where(TimelineItem.timeline_id == timeline_id).order_by(desc(TimelineItem.date)))
    return result.scalars().all()

async def create_timeline_item(
    db: AsyncSession,
    item_in: TimelineItemCreate,
    timeline_id: int
) -> TimelineItem:
    db_item = TimelineItem(
        **item_in.model_dump(),
        timeline_id=timeline_id
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_timeline_item(
    db: AsyncSession,
    item: TimelineItem,
    item_in: TimelineItemUpdate
) -> TimelineItem:
    
    update_data = item_in.model_dump(exclude_unset=True)
    
    # Se video_url for definido, limpa image_url
    if 'video_url' in update_data and update_data['video_url'] is not None:
        update_data['image_url'] = None
    
    # Se image_url for definido, limpa video_url
    if 'image_url' in update_data and update_data['image_url'] is not None:
        update_data['video_url'] = None
    
    for field, value in update_data.items():
        setattr(item, field, value)

    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return item

async def delete_timeline_item(db: AsyncSession, item_id: int) -> Optional[TimelineItem]:
    item = await get_timeline_item(db=db, item_id=item_id)
    if item:
        await db.delete(item)
        await db.commit()
        return item
    return None 