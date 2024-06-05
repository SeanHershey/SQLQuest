from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    TODO: Reset
    """
    quest_ledger_reset_sql = "TRUNCATE quest_ledger RESTART IDENTITY CASCADE"
    gold_ledger_reset_sql = "TRUNCATE gold_ledger RESTART IDENTITY CASCADE"
    stock_reset_sql = "TRUNCATE stock RESTART IDENTITY CASCADE"
    game_log_reset_sql = "TRUNCATE game_log RESTART IDENTITY CASCADE"
    characters_reset_sql = "TRUNCATE characters RESTART IDENTITY CASCADE"
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(quest_ledger_reset_sql))
        connection.execute(sqlalchemy.text(gold_ledger_reset_sql))
        connection.execute(sqlalchemy.text(stock_reset_sql))
        connection.execute(sqlalchemy.text(game_log_reset_sql))
        connection.execute(sqlalchemy.text(characters_reset_sql))
    return {"success": True}

