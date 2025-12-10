from typing import List
from fastapi import APIRouter
from schemas.inventory import Inventory, InventoryBase, InventoryCreate
router = APIRouter()

test_inventory = [
    Inventory(inventory_id=1, name="Ebony Dagger", quantity=1, price=99.99)
]

@router.get("/inventory", response_model=List[Inventory])
async def get_inventory():
    return test_inventory

@router.post("/inventory", response_model=Inventory)
async def create_inventory(inventory: InventoryCreate):
    new_inventory_id = max(inventory.inventory_id for inventory in test_inventory) + 1
    new_inventory = Inventory(inventory_id=new_inventory_id, **inventory.model_dump())
    test_inventory.append(new_inventory)
    return new_inventory
