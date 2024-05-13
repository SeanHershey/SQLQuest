from fastapi import APIRouter, HTTPException, status
import sqlalchemy
from src import database as db
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    item_id: int
    item_name: str
    quantity: int
    equipped: int

@router.get("/inventory/{char_id}", tags=["inventory"])
def get_inventory(char_id: int):
    return "not implemented"

@router.post("/equip/{char_id}/{item_id}", tags=["inventory"])
def equip_item(char_id: int, item_id: int):
    return "not implemented"