from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.gift_shop import GiftShop, GiftProduct, GiftShopBuyProduct
from app.schemas.gift_shop import GiftShopBuyProduct as GiftShopBuyProductSchema, GiftShopCreate, GiftShopUpdate, GiftProductCreate, GiftProductUpdate, GiftShopBuyProductUpdate
from app.crud import guest as guest_crud, user as user_crud
from app.errors.base import create_already_exists_error, create_not_found_error
from app.services.pix import PayloadPixGen

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
    user_id: int
) -> Optional[GiftShop]:
    result = await db.execute(
        select(GiftShop).where(
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
    product_in: GiftProductCreate,
    shop_id: int
) -> GiftProduct:
    db_item = GiftProduct(
        **product_in.model_dump(),
        shop_id=shop_id
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_gift_product(
    db: AsyncSession,
    product: GiftProduct,
    product_in: GiftProductUpdate
) -> GiftProduct:
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def delete_gift_product(
    db: AsyncSession,
    product_id: int,
) -> Optional[GiftProduct]:
    result = await db.execute(
        select(GiftProduct).where(
            GiftProduct.id == product_id,
        )
    )
    product = result.scalar_one_or_none()
    
    if product:
        await db.delete(product)
        await db.commit()
    
    return product

async def create_gift_shop_buy_product(db: AsyncSession, product_id: int, guest_id: int) -> Optional[GiftShopBuyProduct]:
    buy_product = await get_gift_shop_buy_product(db=db, product_id=product_id, guest_id=guest_id)
    if buy_product:
       return buy_product
    
    db_item = GiftShopBuyProduct(
        product_id=product_id,
        guest_id=guest_id,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_gift_shop_buy_product(db: AsyncSession, product_id: int, guest_id: int) -> Optional[GiftShopBuyProduct]:
    result = await db.execute(select(GiftShopBuyProduct).where(GiftShopBuyProduct.product_id == product_id, GiftShopBuyProduct.guest_id == guest_id))
    return result.scalar_one_or_none()

async def update_gift_shop_buy_product(db: AsyncSession, product_id: int, guest_hash: str, is_payed: bool) -> Optional[GiftShopBuyProduct]:
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise create_not_found_error(
            resource_type="Convite",
            resource_id=guest_hash
        )
    
    buy_product = await get_gift_shop_buy_product(db=db, product_id=product_id, guest_id=guest.id)
    if not buy_product:
        raise create_not_found_error(
            resource_type="Compra",
            resource_id=product_id
        )
    
    if is_payed:
        buy_product.payed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        buy_product.payed = True
    else:
        buy_product.payed_at = None
        buy_product.payed = False
    
    db.add(buy_product)
    await db.commit()
    await db.refresh(buy_product)
    return buy_product

async def get_gift_shop_by_guest_hash(db: AsyncSession, guest_hash: str) -> Optional[GiftShop]:
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise create_not_found_error(
            resource_type="Convite",
            resource_id=guest_hash
        )
    
    stmt = (
        select(GiftShop)
        .options(
            selectinload(GiftShop.products)
            .selectinload(GiftProduct.buy_products)
            .selectinload(GiftShopBuyProduct.guest)
        )
        .where(GiftShop.user_id == guest.user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def buy_gift_product(db: AsyncSession, product_id: int, guest_hash: str) -> Optional[GiftShopBuyProductSchema]:

    product = await get_gift_product(db=db, product_id=product_id)
    if not product:
        raise create_not_found_error(
            resource_type="Produto",
            resource_id=product_id
        )
    
    shop = await get_gift_shop_by_guest_hash(db=db, guest_hash=guest_hash)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=guest_hash
        )
    
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise create_not_found_error(
            resource_type="Convite",
            resource_id=guest_hash
        )
    
    user = await user_crud.get_user_by_id(db=db, user_id=shop.user_id)
    if not user:
        raise create_not_found_error(
            resource_type="Usuário",
            resource_id=shop.user_id
        )
    
    buy_product = await create_gift_shop_buy_product(db=db, product_id=product_id, guest_id=guest.id)
    
    codigo_pix = PayloadPixGen(
        valor=str(product.price),
        name=user.full_name,
        key=shop.pix_key,
        city="ANANINDEUA",
        description=guest.hash_link
    ).PayloadFull
    
    return GiftShopBuyProductSchema(
        codigo_pix=codigo_pix,
        product=product,
        user=user,
        guest=guest,
        buy_product=buy_product
    )