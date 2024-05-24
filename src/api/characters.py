from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.post("/character", tags=["characters"])
def create_character(name: str):
    """
    TODO: Create Character
    """

    with db.engine.begin() as connection:
        ID = connection.execute(sqlalchemy.text(
            """
                INSERT INTO characters (name) VALUES (:name) RETURNING ID
            """)
            ,{'name': name}).scalar_one()

    return ID

@router.post("/character/rename", tags=["characters"])
def rename_character(charID: int, name: str):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
                UPDATE characters SET name = :name WHERE ID = :CharID
            """)
            ,{'CharID': charID, 'name': name})
    
    return {"success": True}

@router.post("/character/inventory", tags=["characters"])
def character_start_inventory(charID: int):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
                INSERT INTO inventory (equipped, quantity, char_id, item_id) VALUES (false, 1, :CharID, 1), (false, 1, :CharID, 2)
            """)
            ,{'CharID': charID})
    
    return {"success": True}
