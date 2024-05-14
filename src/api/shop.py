from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from src.api import auth
from typing import List
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
    dependencies=[Depends(auth.get_api_key)],
)

class Item(BaseModel):
    item_id: int
    item_name: str
    quantity: int
    equipped: int

@router.get("/shop", tags=["shop"])
def get_shop(shop_id: int):
    """Get all items in the shop."""
    get_shop_sql = "SELECT stock.item_id as item_id, items.item_name as item_name, COALESCE(SUM(stock.quantity),0) as quantity, items.sell_price as price FROM stock JOIN items ON stock.item_id = items.item_id WHERE stock.shop_id = :shop_id"
    with db.engine.connect() as connection:
        result = connection.execute(
            sqlalchemy.text(get_shop_sql),
            {"shop_id": shop_id}
        )
        store = []
        for row in result:
            store.append({
                "item_id": row.item_id,
                "item_name": row.item_name,
                "quantity": row.quantity,
                "price": row.price
            })
    return store

@router.post("/shop/{shop_id}/{char_id}/{item_id}", tags=["shop"])
def buy_item(char_id: int, item_id: int, quantity: int):
    """Buy an item from the shop."""
    stock_insert_sql = "INSERT INTO stock (shop_id, item_id, quantity) VALUES (:shop_id, :item_id, :quantity)"
    gold_insert_sql = "INSERT INTO gold_ledger (gold, char_id) VALUES (:gold, :char_id)"
    with db.engine.connect() as connection:
        connection.execute(
            sqlalchemy.text(stock_insert_sql),
            [{
                "shop_id": 1,
                "item_id": item_id,
                "quantity": quantity,
            }]
        )
        connection.execute(
            sqlalchemy.text(gold_insert_sql),
            [{
                "gold": -1,
                "char_id": char_id,
            }]
        )
    return "not implemented"

@router.post("/shop/{shop_id}", tags=["shop"])
def stock_shop(shop_id: int, items: List[Item]):
    """Stock the shop with items."""
    insert_item_sql = "INSERT INTO stock (shop_id, item_id, quantity) VALUES (:shop_id, :item_id, :quantity)"
    with db.engine.connect() as connection:
        for item in items:
            connection.execute(
                sqlalchemy.text(insert_item_sql),
                [{
                    "shop_id": shop_id,
                    "item_id": item.item_id,
                    "quantity": item.quantity,
                }]
            )
        return "success"
    return "failure"