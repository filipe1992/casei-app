from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.gift_shop import GiftShop, GiftProduct, GiftShopPurchase
from app.schemas.gift_shop import GiftShopPurchase as GiftShopPurchaseSchema, GiftShopCreate, GiftShopUpdate, GiftProductCreate, GiftProductUpdate, GiftShopPurchaseUpdate
from app.crud import guest as guest_crud, user as user_crud
from app.errors.base import create_not_found_error
from app.services.pix import PayloadPixGen
from app.services.whatsapp import get_whatsapp_service

# Shop Operations

async def get_gift_shop(db: AsyncSession, shop_id: int) -> Optional[GiftShop]:
    result = await db.execute(
        select(GiftShop)
        .options(
            selectinload(GiftShop.products)
            .selectinload(GiftProduct.photo)
        )
        .where(GiftShop.id == shop_id)
    )
    return result.scalar_one_or_none()

async def get_user_gift_shop(db: AsyncSession, user_id: int) -> Optional[GiftShop]:
    stmt = (
        select(GiftShop)
        .options(
            selectinload(GiftShop.products)
            .selectinload(GiftProduct.photo)
        )
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

# Product Operations

async def get_gift_product(db: AsyncSession, product_id: int) -> Optional[GiftProduct]:
    result = await db.execute(
        select(GiftProduct)
        .options(selectinload(GiftProduct.photo))
        .where(GiftProduct.id == product_id)
    )
    return result.scalar_one_or_none()

async def get_shop_products(
    db: AsyncSession,
    shop_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[GiftProduct]:
    result = await db.execute(
        select(GiftProduct)
        .options(selectinload(GiftProduct.photo))
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
    return await get_gift_product(db=db, product_id=db_item.id)

async def update_gift_product(
    db: AsyncSession,
    product: GiftProduct,
    product_in: GiftProductUpdate
) -> GiftProduct:
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "photo_id" and product.image:
            product.image = None
        elif field == "image" and product.photo_id:
            product.photo_id = None
        setattr(product, field, value)
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return await get_gift_product(db=db, product_id=product.id)

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

async def create_gift_shop_purchase(db: AsyncSession, product_id: int, guest_id: int) -> Optional[GiftShopPurchase]:
    purchase = await get_gift_shop_purchase(db=db, product_id=product_id, guest_id=guest_id)
    if purchase:
       return purchase
    
    db_item = GiftShopPurchase(
        product_id=product_id,
        guest_id=guest_id,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_gift_shop_purchase(db: AsyncSession, product_id: int, guest_id: int) -> Optional[GiftShopPurchase]:
    result = await db.execute(select(GiftShopPurchase).where(GiftShopPurchase.product_id == product_id, GiftShopPurchase.guest_id == guest_id))
    return result.scalar_one_or_none()

async def update_gift_shop_purchase(db: AsyncSession, product_id: int, guest_hash: str, is_paid: bool) -> Optional[GiftShopPurchase]:
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise create_not_found_error(
            resource_type="Invitation",
            resource_id=guest_hash
        )
    
    purchase = await get_gift_shop_purchase(db=db, product_id=product_id, guest_id=guest.id)
    if not purchase:
        raise create_not_found_error(
            resource_type="Purchase",
            resource_id=product_id
        )
    
    if is_paid:
        purchase.paid_at = datetime.now(timezone.utc).replace(tzinfo=None)
        purchase.paid = True
        whatsapp = get_whatsapp_service()
        await whatsapp.send_message(guest.phone.replace("+", ""), f"Obrigado {guest.name}!\nDesde ja agradecemos pelo presente!, que Deus abençoe a sua vida!\n\n Te esperamos no casamento!")
    else:
        purchase.paid_at = None
        purchase.paid = False
    
    db.add(purchase)
    await db.commit()
    await db.refresh(purchase)
    return purchase

async def get_gift_shop_by_guest_hash(db: AsyncSession, guest_hash: str) -> Optional[GiftShop]:
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise create_not_found_error(
            resource_type="Invitation",
            resource_id=guest_hash
        )
    
    stmt = (
        select(GiftShop)
        .options(
            selectinload(GiftShop.products)
            .selectinload(GiftProduct.photo),
            selectinload(GiftShop.products)
            .selectinload(GiftProduct.purchases)
            .selectinload(GiftShopPurchase.guest)
        )
        .where(GiftShop.user_id == guest.user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def purchase_gift_product(db: AsyncSession, product_id: int, guest_hash: str) -> Optional[GiftShopPurchaseSchema]:
    
    product = await get_gift_product(db=db, product_id=product_id)
    if not product:
        raise create_not_found_error(
            resource_type="Product",
            resource_id=product_id
        )
    
    shop = await get_gift_shop_by_guest_hash(db=db, guest_hash=guest_hash)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=guest_hash
        )
    
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise create_not_found_error(
            resource_type="Invitation",
            resource_id=guest_hash
        )
    
    user = await user_crud.get_user_with_configuration_by_id(db=db, user_id=shop.user_id)
    if not user:
        raise create_not_found_error(
            resource_type="User",
            resource_id=shop.user_id
        )
    
    purchase = await create_gift_shop_purchase(db=db, product_id=product_id, guest_id=guest.id)
    
    pix_code = PayloadPixGen(
        valor=str(product.price),
        name=user.full_name,
        key=user.configuration.pix_key,
        city=user.configuration.pix_city,
        description=guest.hash_link
    ).PayloadFull
    
    return GiftShopPurchaseSchema(
        pix_code=pix_code,
        product=product,
        user=user,
        guest=guest,
        purchase=purchase
    )