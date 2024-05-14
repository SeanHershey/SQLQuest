from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()


@router.post("/signup/", tags=["users"])
def create_user(username: str):
    """
    Signup User 
    """

    with db.engine.begin() as connection:
        new_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO users (username) VALUES (:username) RETURNING ID
            """),
            {'username': username}).scalar_one()

    return new_id



@router.get("/users/", tags=["users"])
def get_users():
    """
    Get Users
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