from typing import Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.crud import gift_shop as gift_shop_crud
from app.schemas.gift_shop import (
    GiftShop,
    GiftShopBase,
    GiftShopPurchaseBase,
    GiftShopCreate,
    GiftShopUpdate,
    GiftProduct,
    GiftProductCreate,
    GiftProductUpdate,
    GiftShopPurchase,
    GiftShopWithProducts
)
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user
from app.errors.base import (
    create_not_found_error,
    create_already_exists_error,
    create_validation_error,
    create_access_denied_error,
    ErrorCode
)

router = APIRouter()

# Shop Routes

@router.post(
    "/",
    response_model=GiftShopBase,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Shop created successfully"},
        400: {"description": "Business error"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def create_gift_shop(
    shop_in: GiftShopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new gift shop.
    
    - Each user can have only one shop
    - A name is required
    """
    existing_shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if existing_shop:
        raise create_already_exists_error(
            resource_type="Loja de Presentes",
            identifier=current_user.id
        )
    
    shop = await gift_shop_crud.create_gift_shop(
        db=db,
        shop_in=shop_in,
        user_id=current_user.id
    )
    return shop

@router.get(
    "/me",
    response_model=GiftShop,
    responses={
        200: {"description": "Shop retrieved successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def read_gift_shop(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user's gift shop.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    return shop

@router.put(
    "/me",
    response_model=GiftShop,
    responses={
        200: {"description": "Shop updated successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def update_gift_shop(
    shop_in: GiftShopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update current user's gift shop.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    
    shop = await gift_shop_crud.update_gift_shop(
        db=db,
        shop=shop,
        shop_in=shop_in
    )
    return shop

@router.delete(
    "/me",
    response_model=GiftShop,
    responses={
        200: {"description": "Shop deleted successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def delete_gift_shop(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete current user's gift shop.
    
    - This operation also removes all associated products
    """
    shop = await gift_shop_crud.delete_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    return shop

# Product Routes

@router.post(
    "/me/products",
    response_model=GiftProduct,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Product created successfully"},
        400: {"description": "Business error"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def create_gift_product(
    product_in: GiftProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new product in current user's shop.
    
    Validation rules:
    - Name is required
    - Price is required and must be positive
    - Photo ID is optional
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    
    try:
        product = await gift_shop_crud.create_gift_product(
            db=db,
            product_in=product_in,
            shop_id=shop.id
        )
        return product
    except ValidationError as e:
        raise create_validation_error(
            error_code=ErrorCode.INVALID_CONTENT,
            message="Product data validation error",
            validation_errors=e.errors()
        )

@router.get(
    "/me/products",
    response_model=List[GiftProduct],
    responses={
        200: {"description": "Products retrieved successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def read_gift_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    List all products from current user's shop.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    
    return await gift_shop_crud.get_shop_products(db=db, shop_id=shop.id)

@router.put(
    "/me/products/{product_id}",
    response_model=GiftProduct,
    responses={
        200: {"description": "Product updated successfully"},
        400: {"description": "Business error"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def update_gift_product(
    product_id: int,
    product_in: GiftProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a specific product from current user's shop.
    
    - All fields are optional for update
    - Photo ID is optional
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    
    product = await gift_shop_crud.get_gift_product(db=db, product_id=product_id)
    if not product:
        raise create_not_found_error(
            resource_type="Product",
            resource_id=product_id
        )
    
    if product.shop_id != shop.id:
        raise create_access_denied_error(
            resource_type="Product",
            resource_id=product_id
        )
    
    try:
        product = await gift_shop_crud.update_gift_product(
            db=db,
            product=product,
            product_in=product_in
        )
        return product
    except ValidationError as e:
        raise create_validation_error(
            error_code=ErrorCode.INVALID_CONTENT,
            message="Product data validation error",
            validation_errors=e.errors()
        )

@router.delete(
    "/me/products/{product_id}",
    response_model=GiftProduct,
    responses={
        200: {"description": "Product deleted successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def delete_gift_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a specific product from current user's shop.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=current_user.id
        )
    
    product = await gift_shop_crud.get_gift_product(db=db, product_id=product_id)
    if not product:
        raise create_not_found_error(
            resource_type="Product",
            resource_id=product_id
        )
    
    if product.shop_id != shop.id:
        raise create_access_denied_error(
            resource_type="Product",
            resource_id=product_id
        )
    
    product = await gift_shop_crud.delete_gift_product(db=db, product_id=product_id)
    return product 

@router.get(
    "/guest/{guest_hash}",
    response_model=GiftShopWithProducts,
    responses={
        200: {"description": "Shop retrieved successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def read_gift_shop_by_guest_hash(
    guest_hash: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get gift shop by guest hash.
    """
    shop = await gift_shop_crud.get_gift_shop_by_guest_hash(db=db, guest_hash=guest_hash)
    if not shop:
        raise create_not_found_error(
            resource_type="Gift Shop",
            resource_id=guest_hash
        )
    return shop

@router.get(
    "/purchase/{product_id}/guest/{guest_hash}",
    response_model=GiftShopPurchase,
    responses={
        200: {"description": "Purchase created successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def purchase_gift_product(
    product_id: int,
    guest_hash: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Purchase a product from the gift shop.
    """
    return await gift_shop_crud.purchase_gift_product(db=db, product_id=product_id, guest_hash=guest_hash)

@router.put(
    "/purchase/{product_id}/guest/{guest_hash}/paid/{is_paid}",
    response_model=GiftShopPurchaseBase,
    responses={
        200: {"description": "Purchase status updated successfully"},
        404: {"description": "Resource not found"},
        500: {"description": "System error"}
    }
)
async def update_gift_shop_purchase(
    product_id: int,
    guest_hash: str,
    is_paid: bool,
    db: Session = Depends(get_db),
) -> Any:
    """
    Update payment status of a gift shop purchase.
    """
    return await gift_shop_crud.update_gift_shop_purchase(db=db, product_id=product_id, guest_hash=guest_hash, is_paid=is_paid)