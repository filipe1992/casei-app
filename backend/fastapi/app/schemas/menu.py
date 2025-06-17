from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# MenuItem Schemas
class MenuItemBase(BaseModel):
    name: str = Field(..., description="Nome do item do cardápio")
    description: Optional[str] = Field(None, description="Descrição detalhada do item")
    restrictions: Optional[str] = Field(None, description="Restrições alimentares (ex: lactose, glúten)")
    calories: Optional[int] = Field(None, description="Quantidade de calorias")
    observations: Optional[str] = Field(None, description="Observações sobre o preparo ou consumo")

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    name: Optional[str] = Field(None, description="Nome do item do cardápio")

class MenuItem(MenuItemBase):
    id: int
    menu_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Menu Schemas
class MenuBase(BaseModel):
    title: str = Field(..., description="Título do cardápio")

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    title: Optional[str] = Field(None, description="Título do cardápio")

class MenuResponse(MenuBase):
    id: int
    user_id: int
    items: List[MenuItem]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class Menu(MenuBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 