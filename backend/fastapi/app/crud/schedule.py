from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.schedule import Schedule, ScheduleItem
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleItemCreate, ScheduleItemUpdate

async def create_schedule(db: AsyncSession, *, obj_in: ScheduleCreate, user_id: int) -> Schedule:
    """
    Cria um novo cronograma com seus itens em uma única transação.
    
    Args:
        db: Sessão assíncrona do banco de dados
        obj_in: Dados do cronograma e seus itens
        user_id: ID do usuário que está criando o cronograma
        
    Returns:
        Schedule: Objeto do cronograma criado com seus itens
    """
    # Cria o objeto do cronograma com seus itens
    db_obj = Schedule(
        title=obj_in.title,
        user_id=user_id,
        data_casamento=obj_in.data_casamento,
        items=[
            ScheduleItem(
                title=item.title,
                description=item.description,
                time=item.time
            )
            for item in obj_in.items
        ]
    )
    
    # Adiciona e comita
    db.add(db_obj)
    await db.commit()
    
    # Recarrega o objeto com os itens
    return await get_schedule(db=db, user_id=user_id)

async def get_schedule(db: AsyncSession, user_id: int) -> Optional[Schedule]:
    """Obtém o cronograma de um usuário"""
    result = await db.execute(
        select(Schedule)
        .options(selectinload(Schedule.items))
        .filter(Schedule.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def update_schedule(
    db: AsyncSession, *, db_obj: Schedule, obj_in: ScheduleUpdate
) -> Schedule:
    """Atualiza o título do cronograma"""
    db_obj.title = obj_in.title
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def delete_schedule(db: AsyncSession, *, db_obj: Schedule) -> None:
    """Deleta um cronograma e todos seus itens"""
    await db.delete(db_obj)
    await db.commit()

async def create_schedule_item(
    db: AsyncSession, *, schedule_id: int, obj_in: ScheduleItemCreate
) -> ScheduleItem:
    """Adiciona um novo item ao cronograma"""
    db_obj = ScheduleItem(
        schedule_id=schedule_id,
        title=obj_in.title,
        description=obj_in.description,
        time=obj_in.time
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update_schedule_item(
    db: AsyncSession, *, db_obj: ScheduleItem, obj_in: ScheduleItemUpdate
) -> ScheduleItem:
    """Atualiza um item do cronograma"""
    db_obj.title = obj_in.title
    db_obj.description = obj_in.description
    db_obj.time = obj_in.time
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def delete_schedule_item(db: AsyncSession, *, db_obj: ScheduleItem) -> None:
    """Remove um item do cronograma"""
    await db.delete(db_obj)
    await db.commit()

async def get_schedule_item(db: AsyncSession, item_id: int) -> Optional[ScheduleItem]:
    """Obtém um item específico do cronograma"""
    result = await db.execute(
        select(ScheduleItem)
        .filter(ScheduleItem.id == item_id)
    )
    return result.scalar_one_or_none() 