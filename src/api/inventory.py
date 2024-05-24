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
    print("in get inv")
    with db.engine.begin() as connection:
        inventory = connection.execute(sqlalchemy.text(
            """
            SELECT *
            FROM inventory
            JOIN items ON inventory.item_id = items.id
            WHERE inventory.char_id = :char_id
            """
        ), {"char_id": char_id})
    output = []
    for item in inventory:
            output.append(
                 {
                    "item_id": item.id,
                    "item_name": item.name,
                    "quantity": item.quantity,
                    "equipped": item.equipped, 
                    "equip_slot": item.equip_slot
                 }
            )
    return output

    

@router.post("/equip/{char_id}/{item_id}", tags=["inventory"])
def equip_item(char_id: int, item_id: int):
        status_string = ""
        with db.engine.begin() as connection:
            # get item details
            
            item_result = connection.execute(sqlalchemy.text(
                """
                SELECT inventory.equipped, items.equip_slot, items.name
                FROM inventory
                JOIN items ON inventory.item_id = items.id
                WHERE inventory.char_id = :char_id AND inventory.item_id = :item_id
                """
                ), {"char_id": char_id, "item_id": item_id}).fetchone()
            character_name = connection.execute(sqlalchemy.text(
                """
                SELECT name
                FROM characters
                WHERE id = :char_id
                """
            ), {"char_id": char_id}).fetchone()
            if not item_result:
                error = "Item not found in inventory"
                print(error)
                return {"success": False}

            equipped, equip_slot, item_name = item_result
            # If the item is already equipped, unequip it
            if equipped:
                connection.execute(sqlalchemy.text(
                    """
                    UPDATE inventory
                    SET equipped = FALSE
                    WHERE char_id = :char_id AND item_id = :item_id
                    """
                ), {"char_id": char_id, "item_id": item_id})
                status_string += item_name + " un-equipped from character: "+ character_name.name + " from slot: "+ equip_slot + " "
            
            # Check for conflicts in the same equip slot
            conflict = connection.execute(sqlalchemy.text(
                """
                SELECT inventory.item_id, items.name
                FROM inventory
                JOIN items ON inventory.item_id = items.id
                WHERE inventory.char_id = :char_id AND items.equip_slot = :equip_slot AND inventory.equipped = TRUE
                """
            ), {"char_id": char_id, "equip_slot": equip_slot}).fetchone()
            
            if conflict:
                # Unequip the conflicting item
                connection.execute(sqlalchemy.text(
                    """
                    UPDATE inventory
                    SET equipped = 0
                    WHERE char_id = :char_id AND item_id = :conflicting_item_id
                    """
                ), {"char_id": char_id, "conflicting_item_id": conflict.item_id})

                status_string +=  conflict.name + " un-equipped from character: " + character_name.name + " from slot: "+ equip_slot
            # Equip the original item
            connection.execute(sqlalchemy.text(
                """
                UPDATE inventory
                SET equipped = TRUE
                WHERE char_id = :char_id AND item_id = :item_id
                """
            ), {"char_id": char_id, "item_id": item_id})
            status_string +=  item_name + " equipped to character: "+character_name.name + " to slot: "+ equip_slot 
            print(status_string)
            if status_string == "":
                return {"success": False}
            else:
                connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO game_log (description, char_id) 
                    VALUES (:description, :char_id)
                    """
                ), { "description": status_string, "char_id": char_id})
                return {"success": True}

