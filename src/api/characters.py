from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.post("/", tags=["characters"])
def create_character():
    """
    TODO: Create Character
    """

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
                INSERT INTO characters (name) VALUES (test)
            """))

    return "OK"


@router.get("/characters/", tags=["characters"])
def get_characters():
    """
    TODO: Get Characters
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
                SELECT * FROM characters
            """))

    json = []
    for character in result:
        json.append(
            {
                "name": character.name})

    return result