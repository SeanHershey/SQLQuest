from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.post("/signup", tags=["users"])
def create_user(username: str, password: str):
    """
    TODO: Create Character
    """

    with db.engine.begin() as connection:
        new_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO users (username, password) VALUES (:username, :password) RETURNING ID
            """),
            {'username': username, 'password': password}).scalar_one()

    return new_id



@router.get("/users/", tags=["users"])
def get_users():
    """
    TODO: Get Characters
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
                SELECT * FROM users
            """))

    json = []
    for character in result:
        json.append(
            {
                "name": character.name})

    return result