from typing import Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.crud import gift_shop as gift_shop_crud
from app.schemas.gift_shop import (
    GiftShop,
    GiftShopBase,
    GiftShopBuyProductBase,
    GiftShopCreate,
    GiftShopUpdate,
    GiftProduct,
    GiftProductCreate,
    GiftProductUpdate,
    GiftShopBuyProduct,
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

# Rotas da Loja

@router.post(
    "/",
    response_model=GiftShopBase,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Loja criada com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def create_gift_shop(
    shop_in: GiftShopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar nova loja de presentes.
    
    - Cada usuário só pode ter uma loja
    - É necessário fornecer um nome e uma chave PIX
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
        200: {"description": "Loja recuperada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def read_gift_shop(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar a loja de presentes do usuário atual.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=current_user.id
        )
    return shop

@router.put(
    "/me",
    response_model=GiftShop,
    responses={
        200: {"description": "Loja atualizada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def update_gift_shop(
    shop_in: GiftShopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar a loja de presentes do usuário atual.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
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
        200: {"description": "Loja deletada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def delete_gift_shop(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar a loja de presentes do usuário atual.
    
    - A operação também remove todos os produtos associados
    """
    shop = await gift_shop_crud.delete_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=current_user.id
        )
    return shop

# Rotas de Produtos

@router.post(
    "/me/products",
    response_model=GiftProduct,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Produto criado com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def create_gift_product(
    product_in: GiftProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar novo produto na loja do usuário atual.
    
    Regras de validação:
    - Nome é obrigatório
    - Preço é obrigatório e deve ser positivo
    - Imagem é obrigatória e deve estar em formato base64
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
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
            message="Erro de validação dos dados do produto",
            validation_errors=e.errors()
        )

@router.get(
    "/me/products",
    response_model=List[GiftProduct],
    responses={
        200: {"description": "Produtos recuperados com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def read_gift_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Listar todos os produtos da loja do usuário atual.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=current_user.id
        )
    
    return await gift_shop_crud.get_shop_products(db=db, shop_id=shop.id)

@router.put(
    "/me/products/{product_id}",
    response_model=GiftProduct,
    responses={
        200: {"description": "Produto atualizado com sucesso"},
        400: {"description": "Erro de negócio"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def update_gift_product(
    product_id: int,
    product_in: GiftProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um produto específico da loja do usuário atual.
    
    - Todos os campos são opcionais na atualização
    - Se fornecida, a imagem deve estar em formato base64
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=current_user.id
        )
    
    product = await gift_shop_crud.get_gift_product(db=db, product_id=product_id)
    if not product:
        raise create_not_found_error(
            resource_type="Produto",
            resource_id=product_id
        )
    
    if product.shop_id != shop.id:
        raise create_access_denied_error(
            resource_type="Produto",
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
            message="Erro de validação dos dados do produto",
            validation_errors=e.errors()
        )

@router.delete(
    "/me/products/{product_id}",
    response_model=GiftProduct,
    responses={
        200: {"description": "Produto deletado com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def delete_gift_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um produto específico da loja do usuário atual.
    """
    shop = await gift_shop_crud.get_user_gift_shop(db=db, user_id=current_user.id)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=current_user.id
        )
    
    product = await gift_shop_crud.get_gift_product(db=db, product_id=product_id)
    if not product:
        raise create_not_found_error(
            resource_type="Produto",
            resource_id=product_id
        )
    
    if product.shop_id != shop.id:
        raise create_access_denied_error(
            resource_type="Produto",
            resource_id=product_id
        )
    
    product = await gift_shop_crud.delete_gift_product(db=db, product_id=product_id)
    return product 

@router.get(
    "/guest/{guest_hash}",
    response_model=GiftShopWithProducts,
    responses={
        200: {"description": "Loja recuperada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def read_gift_shop_by_guest_hash(
    guest_hash: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Recuperar a loja de presentes do usuário atual.
    """
    shop = await gift_shop_crud.get_gift_shop_by_guest_hash(db=db, guest_hash=guest_hash)
    if not shop:
        raise create_not_found_error(
            resource_type="Loja de Presentes",
            resource_id=guest_hash
        )
    return shop


@router.get(
    "/buy-gift/{product_id}/guest/{guest_hash}",
    response_model=GiftShopBuyProduct,
    responses={
        200: {"description": "Loja recuperada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def buy_gift_product(
    product_id: int,
    guest_hash: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Comprar um produto da loja de presentes do usuário atual.
    """
    gift_shop_buy_product = await gift_shop_crud.buy_gift_product(db=db, product_id=product_id, guest_hash=guest_hash)
    
    return gift_shop_buy_product


@router.put(
    "/buy-gift/{product_id}/guest/{guest_hash}/payed/{is_payed}",
    response_model=GiftShopBuyProductBase,
    responses={
        200: {"description": "Loja recuperada com sucesso"},
        404: {"description": "Recurso não encontrado"},
        500: {"description": "Erro do sistema"}
    }
)
async def update_gift_shop_buy_product(
    product_id: int,
    guest_hash: str,
    is_payed: bool,
    db: Session = Depends(get_db),
) -> Any:
    """
    Atualizar o status de pagamento de um produto da loja de presentes do usuário atual.
    """
    gift_shop_buy_product = await gift_shop_crud.update_gift_shop_buy_product(db=db, product_id=product_id, guest_hash=guest_hash, is_payed=is_payed)
    return gift_shop_buy_product