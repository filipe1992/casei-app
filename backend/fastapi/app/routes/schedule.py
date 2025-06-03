from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schedule import (
    Schedule,
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleItemCreate,
    ScheduleItemUpdate,
    ScheduleItemInDB
)
from app.crud import schedule as schedule_crud
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user


router = APIRouter()

@router.post("/", response_model=Schedule)
async def create_schedule(
    *,
    db: AsyncSession = Depends(get_db),
    schedule_in: ScheduleCreate,
    current_user: User = Depends(get_current_user)
) -> Schedule:
    """
    Criar um novo cronograma.
    """
    existing_schedule = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if existing_schedule:
        raise HTTPException(
            status_code=400,
            detail="Usuário já possui um cronograma"
        )
    return await schedule_crud.create_schedule(db=db, obj_in=schedule_in, user_id=current_user.id)

@router.get("/", response_model=Schedule)
async def read_schedule(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Schedule:
    """
    Recuperar o cronograma do usuário.
    """
    db_obj = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Cronograma não encontrado")
    return db_obj

@router.put("/", response_model=Schedule)
async def update_schedule(
    *,
    db: AsyncSession = Depends(get_db),
    schedule_in: ScheduleUpdate,
    current_user: User = Depends(get_current_user)
) -> Schedule:
    """
    Atualizar o cronograma.
    """
    db_obj = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Cronograma não encontrado")
    return await schedule_crud.update_schedule(db=db, db_obj=db_obj, obj_in=schedule_in)

@router.delete("/")
async def delete_schedule(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Deletar o cronograma.
    """
    db_obj = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Cronograma não encontrado")
    await schedule_crud.delete_schedule(db=db, db_obj=db_obj)
    return {"message": "Cronograma deletado com sucesso"}

@router.post("/items", response_model=ScheduleItemInDB)
async def create_schedule_item(
    *,
    db: AsyncSession = Depends(get_db),
    item_in: ScheduleItemCreate,
    current_user: User = Depends(get_current_user)
) -> ScheduleItemInDB:
    """
    Adicionar um novo item ao cronograma.
    """
    db_obj = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Cronograma não encontrado")
    return await schedule_crud.create_schedule_item(db=db, schedule_id=db_obj.id, obj_in=item_in)

@router.put("/items/{item_id}", response_model=ScheduleItemInDB)
async def update_schedule_item(
    *,
    db: AsyncSession = Depends(get_db),
    item_id: int,
    item_in: ScheduleItemUpdate,
    current_user: User = Depends(get_current_user)
) -> ScheduleItemInDB:
    """
    Atualizar um item do cronograma.
    """
    db_obj = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Cronograma não encontrado")
    
    item = await schedule_crud.get_schedule_item(db=db, item_id=item_id)
    if not item or item.schedule_id != db_obj.id:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    return await schedule_crud.update_schedule_item(db=db, db_obj=item, obj_in=item_in)

@router.delete("/items/{item_id}")
async def delete_schedule_item(
    *,
    db: AsyncSession = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Remover um item do cronograma.
    """
    db_obj = await schedule_crud.get_schedule(db=db, user_id=current_user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Cronograma não encontrado")
    
    item = await schedule_crud.get_schedule_item(db=db, item_id=item_id)
    if not item or item.schedule_id != db_obj.id:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    await schedule_crud.delete_schedule_item(db=db, db_obj=item)
    return {"message": "Item removido com sucesso"} 