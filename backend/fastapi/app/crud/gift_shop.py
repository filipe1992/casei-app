from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import base64

from app.models.gift_shop import GiftShop, GiftProduct
from app.schemas.gift_shop import GiftShopCreate, GiftShopUpdate, GiftProductCreate, GiftProductUpdate

# Operações da Loja

async def get_gift_shop(db: AsyncSession, shop_id: int) -> Optional[GiftShop]:
    result = await db.execute(select(GiftShop).where(GiftShop.id == shop_id))
    return result.scalar_one_or_none()

async def get_user_gift_shop(db: AsyncSession, user_id: int) -> Optional[GiftShop]:
    stmt = (
        select(GiftShop)
        .options(selectinload(GiftShop.products))
        .where(GiftShop.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_gift_shop(
    db: AsyncSession,
    shop_in: GiftShopCreate,
    user_id: int
) -> GiftShop:
    db_shop = GiftShop(
        **shop_in.model_dump(),
        user_id=user_id
    )
    db.add(db_shop)
    await db.commit()
    await db.refresh(db_shop)
    return db_shop

async def update_gift_shop(
    db: AsyncSession,
    shop: GiftShop,
    shop_in: GiftShopUpdate
) -> GiftShop:
    update_data = shop_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shop, field, value)
    
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return shop

async def delete_gift_shop(
    db: AsyncSession,
    shop_id: int,
    user_id: int
) -> Optional[GiftShop]:
    result = await db.execute(
        select(GiftShop).where(
            GiftShop.id == shop_id,
            GiftShop.user_id == user_id
        )
    )
    shop = result.scalar_one_or_none()
    
    if shop:
        await db.delete(shop)
        await db.commit()
    
    return shop

# Operações de Produtos

async def get_gift_product(db: AsyncSession, product_id: int) -> Optional[GiftProduct]:
    result = await db.execute(select(GiftProduct).where(GiftProduct.id == product_id))
    return result.scalar_one_or_none()

async def get_shop_products(
    db: AsyncSession,
    shop_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[GiftProduct]:
    result = await db.execute(
        select(GiftProduct)
        .where(GiftProduct.shop_id == shop_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_gift_product(
    db: AsyncSession,
    item_in: GiftProductCreate,
    shop_id: int
) -> GiftProduct:
    db_item = GiftProduct(
        **item_in.model_dump(),
        shop_id=shop_id
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_gift_product(
    db: AsyncSession,
    item: GiftProduct,
    item_in: GiftProductUpdate
) -> GiftProduct:
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def delete_gift_product(
    db: AsyncSession,
    item_id: int,
    shop_id: int
) -> Optional[GiftProduct]:
    result = await db.execute(
        select(GiftProduct).where(
            GiftProduct.id == item_id,
            GiftProduct.shop_id == shop_id
        )
    )
    item = result.scalar_one_or_none()
    
    if item:
        await db.delete(item)
        await db.commit()
    
    return item