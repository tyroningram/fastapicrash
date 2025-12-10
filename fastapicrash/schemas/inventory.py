from pydantic import BaseModel, Field

class InventoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

class Inventory(InventoryBase):
    inventory_id: int = Field(..., description="Unique identifier")

class InventoryCreate(InventoryBase):
    pass


