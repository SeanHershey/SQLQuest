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
            #game log
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

class TradeItem(BaseModel):
    item_id: int
    quantity: int

class TradeOffer(BaseModel):
    offer: list[TradeItem] 
    request: list[TradeItem]

@router.post("/inventory/{char_id_1}/trade/{char_id_2}", tags=["inventory"])
def trade(char_id_1: int, char_id_2: int, trade_offer: TradeOffer):
    success = True
    with db.engine.begin() as connection:
        status_string_1 = ""
        status_string_1 = ""
        success = False
        character_name_1 = connection.execute(sqlalchemy.text(
                """
                SELECT name
                FROM characters
                WHERE id = :char_id
                """
            ), {"char_id": char_id_1}).fetchone()
        
        character_name_2 = connection.execute(sqlalchemy.text(
                """
                SELECT name
                FROM characters
                WHERE id = :char_id
                """
            ), {"char_id": char_id_2}).fetchone()
        
        #check trade valid
        for char_id, items, char_flag in [(char_id_1, trade_offer.offer, 1), (char_id_2, trade_offer.request, 2)]: 
            for item in items:
                item_id, quantity = item["item_id"], item["quantity"]
                item_response = connection.execute(
                    sqlalchemy.text("""
                        SELECT quantity, equipped
                        FROM inventory
                        WHERE char_id = :char_id AND item_id = :item_id
                    """), {"char_id": char_id, "item_id": item_id}
                ).fetchone()
                if not item_response or item_response.quantity < quantity or item_response.equipped == True:
                        #falure case
                        if char_flag == 1:
                            status_string = character_name_1.name + " failed to trade: " + "unable to trade item " + str(item_id)+ " to "+ character_name_2.name
                            status_string_1 += status_string
                            status_string_2 += status_string
                        elif char_flag == 2:
                            status_string = character_name_2.name + " failed to trade: " + "unable to trade item " + str(item_id)+ " to "+ character_name_1.name
                            status_string_1 += status_string
                            status_string_2 += status_string
                        success = False
                
        #on trade success
        for offered, requested in zip(trade_offer.offer, trade_offer.request):

            #modify char 1 inventory
            #subtract offered
            connection.execute(sqlalchemy.text("""
                UPDATE inventory
                SET quantity = quantity - :quantity
                WHERE char_id = :char_id AND item_id = :item_id
            """), {"quantity": offered["quantity"], "char_id": char_id_1, "offered_item_id": offered["item_id"]})
            #add requested
            connection.execute(sqlalchemy.text("""
                UPDATE inventory
                SET quantity = quantity + :quantity
                WHERE char_id = :char_id AND item_id = :item_id
            """), {"quantity": requested["quantity"], "char_id": char_id_1, "item_id": requested["item_id"]})
            status_string_1 += character_name_1.name + " traded " + str(offered["quantity"]) + " of "+ str(offered["item_id"]) +" to " + character_name_2.name + " for " + str(requested["quantity"]) + " of " + str(requested["item_id"])
            

            #modify char 2 inventory
            #subtract requested
            connection.execute(sqlalchemy.text("""
                UPDATE inventory
                SET quantity = quantity - :quantity
                WHERE char_id = :char_id AND item_id = :item_id
            """), {"quantity": requested["quantity"], "char_id": char_id_2, "offered_item_id": requested["item_id"]})
            #add offered
            connection.execute(sqlalchemy.text("""
                UPDATE inventory
                SET quantity = quantity + :quantity
                WHERE char_id = :char_id AND item_id = :item_id
            """), {"quantity": offered["quantity"], "char_id": char_id_2, "item_id": offered["item_id"]})
            status_string_2 += character_name_2.name + " traded " + str(requested["quantity"]) + " of "+ str(requested["item_id"]) +" to " + character_name_1.name + " for " + str(offered["quantity"]) + " of " + str(offered["item_id"])
            
            #add trade to both characters game logs
            print(status_string)
            if status_string_1 and status_string_2:
                connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO game_log (description, char_id) 
                    VALUES (:description, :char_id)
                    """
                ), { "description": status_string_1, "char_id": char_id_1})
                connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO game_log (description, char_id) 
                    VALUES (:description, :char_id)
                    """
                ), { "description": status_string_2, "char_id": char_id_2})
                
                return {"success": success}
            else:
                 return{"success": False}