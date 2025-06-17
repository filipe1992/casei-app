from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import menu as menu_crud
from app.schemas.menu import (
    Menu, MenuCreate, MenuUpdate, MenuResponse,
    MenuItem, MenuItemCreate, MenuItemUpdate
)
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user

router = APIRouter()

# Rotas para Menu
@router.post("/menus/", response_model=MenuResponse)
async def create_menu(
    menu_in: MenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar um novo cardápio.
    """
    menu = await menu_crud.create_menu(db=db, menu_in=menu_in, user_id=current_user.id)
    return menu

@router.get("/menus/me", response_model=List[MenuResponse])
async def read_user_menus(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar todos os cardápios do usuário atual.
    """
    menus = await menu_crud.get_user_menus(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return menus

@router.get("/menus/{menu_id}", response_model=MenuResponse)
async def read_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar um cardápio específico.
    """
    menu = await menu_crud.get_menu(db=db, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    if menu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este cardápio")
    return menu

@router.put("/menus/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu_in: MenuUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um cardápio.
    """
    menu = await menu_crud.get_menu(db=db, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    if menu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este cardápio")
    
    menu = await menu_crud.update_menu(db=db, menu=menu, menu_in=menu_in)
    return menu

@router.delete("/menus/{menu_id}", response_model=Menu)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um cardápio.
    """
    menu = await menu_crud.delete_menu(db=db, menu_id=menu_id, user_id=current_user.id)
    if not menu:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    return menu

# Rotas para MenuItem
@router.post("/menus/{menu_id}/items/", response_model=MenuItem)
async def create_menu_item(
    menu_id: int,
    item_in: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar um novo item no cardápio.
    """
    menu = await menu_crud.get_menu(db=db, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    if menu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este cardápio")
    
    item = await menu_crud.create_menu_item(db=db, menu_id=menu_id, item_in=item_in)
    return item

@router.put("/menus/{menu_id}/items/{item_id}", response_model=MenuItem)
async def update_menu_item(
    menu_id: int,
    item_id: int,
    item_in: MenuItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um item do cardápio.
    """
    menu = await menu_crud.get_menu(db=db, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    if menu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este cardápio")
    
    item = await menu_crud.get_menu_item(db=db, item_id=item_id)
    if not item or item.menu_id != menu_id:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    item = await menu_crud.update_menu_item(db=db, item=item, item_in=item_in)
    return item

@router.delete("/menus/{menu_id}/items/{item_id}", response_model=MenuItem)
async def delete_menu_item(
    menu_id: int,
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um item do cardápio.
    """
    menu = await menu_crud.get_menu(db=db, menu_id=menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Cardápio não encontrado")
    if menu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este cardápio")
    
    item = await menu_crud.get_menu_item(db=db, item_id=item_id)
    if not item or item.menu_id != menu_id:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    item = await menu_crud.delete_menu_item(db=db, item_id=item_id)
    return item 