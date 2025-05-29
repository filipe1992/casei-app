from typing import List, Optional
from sqlalchemy.orm import Session
import base64

from app.models.gift_shop import GiftShop, GiftProduct
from app.schemas.gift_shop import GiftShopCreate, GiftShopUpdate, GiftProductCreate, GiftProductUpdate

# Operações da Loja

def get_gift_shop(db: Session, user_id: int) -> Optional[GiftShop]:
    """Retorna a loja de presentes do usuário."""
    return db.query(GiftShop).filter(GiftShop.user_id == user_id).first()

def create_gift_shop(db: Session, shop_in: GiftShopCreate, user_id: int) -> GiftShop:
    """Cria uma nova loja de presentes."""
    db_shop = GiftShop(
        **shop_in.model_dump(),
        user_id=user_id
    )
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

def update_gift_shop(
    db: Session,
    shop: GiftShop,
    shop_in: GiftShopUpdate
) -> GiftShop:
    """Atualiza uma loja de presentes existente."""
    update_data = shop_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shop, field, value)
    
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop

def delete_gift_shop(db: Session, user_id: int) -> Optional[GiftShop]:
    """Deleta a loja de presentes do usuário."""
    shop = get_gift_shop(db=db, user_id=user_id)
    if shop:
        db.delete(shop)
        db.commit()
        return shop
    return None

# Operações de Produtos

def get_gift_product(db: Session, product_id: int) -> Optional[GiftProduct]:
    """Retorna um produto específico."""
    return db.query(GiftProduct).filter(GiftProduct.id == product_id).first()

def get_gift_products(db: Session, shop_id: int) -> List[GiftProduct]:
    """Retorna todos os produtos de uma loja."""
    return db.query(GiftProduct).filter(GiftProduct.shop_id == shop_id).all()

def create_gift_product(
    db: Session,
    product_in: GiftProductCreate,
    shop_id: int
) -> GiftProduct:
    """Cria um novo produto na loja."""
    # Converte a imagem de base64 para bytes
    image_bytes = base64.b64decode(product_in.image)
    
    # Remove o campo image do dict e adiciona separadamente
    product_data = product_in.model_dump(exclude={'image'})
    db_product = GiftProduct(
        **product_data,
        image=image_bytes,
        shop_id=shop_id
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_gift_product(
    db: Session,
    product: GiftProduct,
    product_in: GiftProductUpdate
) -> GiftProduct:
    """Atualiza um produto existente."""
    update_data = product_in.model_dump(exclude_unset=True)
    
    # Se houver uma nova imagem, converte de base64 para bytes
    if 'image' in update_data:
        update_data['image'] = base64.b64decode(update_data['image'])
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_gift_product(db: Session, product_id: int) -> Optional[GiftProduct]:
    """Deleta um produto específico."""
    product = get_gift_product(db=db, product_id=product_id)
    if product:
        db.delete(product)
        db.commit()
        return product
    return None 