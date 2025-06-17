from typing import List, Optional, Union, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.menu import Menu, MenuItem
from app.schemas.menu import MenuCreate, MenuUpdate, MenuItemCreate, MenuItemUpdate

async def create_menu(db: AsyncSession, *, menu_in: MenuCreate, user_id: int) -> Menu:
    """Cria um novo cardápio."""
    db_menu = Menu(
        title=menu_in.title,
        user_id=user_id
    )
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu

async def get_menu(db: AsyncSession, menu_id: int) -> Optional[Menu]:
    """Recupera um cardápio específico com seus itens."""
    result = await db.execute(
        select(Menu)
        .options(joinedload(Menu.items))
        .filter(Menu.id == menu_id)
    )
    return result.scalar_one_or_none()

async def get_user_menus(
    db: AsyncSession, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Menu]:
    """Recupera todos os cardápios de um usuário."""
    result = await db.execute(
        select(Menu)
        .options(joinedload(Menu.items))
        .filter(Menu.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_menu(
    db: AsyncSession,
    *,
    menu: Menu,
    menu_in: Union[MenuUpdate, Dict[str, Any]]
) -> Menu:
    """Atualiza um cardápio."""
    menu_data = menu_in if isinstance(menu_in, dict) else menu_in.model_dump(exclude_unset=True)
    
    for field, value in menu_data.items():
        setattr(menu, field, value)
    
    await db.commit()
    await db.refresh(menu)
    return menu

async def delete_menu(db: AsyncSession, *, menu_id: int, user_id: int) -> Optional[Menu]:
    """Remove um cardápio."""
    menu = await get_menu(db, menu_id)
    if menu and menu.user_id == user_id:
        await db.delete(menu)
        await db.commit()
        return menu
    return None

# Funções para MenuItem
async def create_menu_item(
    db: AsyncSession, 
    *, 
    menu_id: int, 
    item_in: MenuItemCreate
) -> MenuItem:
    """Cria um novo item no cardápio."""
    db_item = MenuItem(
        menu_id=menu_id,
        name=item_in.name,
        description=item_in.description,
        restrictions=item_in.restrictions,
        calories=item_in.calories,
        observations=item_in.observations
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_menu_item(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    """Recupera um item específico do cardápio."""
    result = await db.execute(
        select(MenuItem)
        .filter(MenuItem.id == item_id)
    )
    return result.scalar_one_or_none()

async def update_menu_item(
    db: AsyncSession,
    *,
    item: MenuItem,
    item_in: Union[MenuItemUpdate, Dict[str, Any]]
) -> MenuItem:
    """Atualiza um item do cardápio."""
    item_data = item_in if isinstance(item_in, dict) else item_in.model_dump(exclude_unset=True)
    
    for field, value in item_data.items():
        if value is not None:
            setattr(item, field, value)
    
    await db.commit()
    await db.refresh(item)
    return item

async def delete_menu_item(db: AsyncSession, *, item_id: int) -> Optional[MenuItem]:
    """Remove um item do cardápio."""
    item = await get_menu_item(db, item_id)
    if item:
        await db.delete(item)
        await db.commit()
        return item
    return None 