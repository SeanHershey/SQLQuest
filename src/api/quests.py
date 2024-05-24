from fastapi import APIRouter
import sqlalchemy
from src import database as db
from enum import Enum

router = APIRouter()

class search_sort_options(str, Enum):
    level = "level"
    gold = "gold"

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"  

@router.get("/quests/", tags=["quests"])
def get_quests(
    levelcap: int, 
    hasitem: bool,
    sort_col: search_sort_options = search_sort_options.level,
    sort_order: search_sort_order = search_sort_order.desc,
               ):
    """
    TODO: Get Quests
    """
    ORDER_STR = " ORDER BY " + sort_col + " " + sort_order + ", quests.id DESC"
    HAS_ITEM_STR = ""
    if hasitem: HAS_ITEM_STR = "AND item_id IS NOT NULL"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
                SELECT name, description, level, gold, item_id FROM quests
                WHERE (level <= :levelcap OR :levelcap < 0)
            """ + HAS_ITEM_STR + ORDER_STR), {'levelcap': levelcap})

    json = []
    for quest in result:
        json.append(
            {
                "name": quest.name,
                "description": quest.description,
                "level": quest.level,
                "gold": quest.gold,
                "itemID": quest.item_id})

    return json

@router.get("/quests/character", tags=["quests"])
def get_character_quest(
    charID: int,
    completed: bool
               ):

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
                SELECT created_at, quests.name AS name, quests.description AS description, quests.level AS level, quests.gold AS gold, quests.item_id AS item_id FROM quest_ledger
                JOIN quests ON quests.id = quest_ledger.quest_id
                WHERE char_id = :charID AND complete = :completed
                
            """), {'charID': charID, 'completed': completed})
        json = []
        for quest in result:
            json.append(
                {
                    "time_started": quest.created_at,
                    "name": quest.name,
                    "description": quest.description,
                    "level": quest.level,
                    "gold": quest.gold,
                    "itemID": quest.item_id})
    return json

@router.post("/quests/begin", tags=["quests"])
def begin_quest(
    charID: int,
    questID: int
               ):
    with db.engine.begin() as connection:
        #CHECK IF CHARACTER IS ALREADY ON QUEST
        check = connection.execute(sqlalchemy.text(
            """
                SELECT * FROM quest_ledger
                WHERE char_id = :charID AND complete = False
                
            """), {'charID': charID})
        if(check.rowcount > 0): 
            connection.execute(sqlalchemy.text(
            """
                INSERT INTO game_log (error_id, char_id, description)
                VALUES (:errorID, :charID, :desc)
                
            """), {'errorID': 100,'charID': charID, 'desc': "INVALID BEGIN QUEST REQUEST: " + str(questID)})
            print("CHARACTER ALREADY ON QUEST")
            return "CHARACTER ALREADY ON QUEST"
        
        #ADD TO QUEST LEDGER
        connection.execute(sqlalchemy.text(
            """
                INSERT INTO quest_ledger
                (char_id, quest_id, complete) 
                VALUES (:charID, :questID, :completed)
                
            """), {'charID': charID, 'questID': questID, 'completed': False})
        connection.execute(sqlalchemy.text(
            """
                INSERT INTO game_log (error_id, char_id, description)
                VALUES (:errorID, :charID, :desc)
                
            """), {'errorID': 0,'charID': charID, 'desc': "QUEST BEGAN: " + str(questID)})
    
    return {"success": True}

@router.post("/quests/complete", tags=["quests"])
def complete_quest(
    charID: int
               ):
    with db.engine.begin() as connection:
        #CHECK IF CHARACTER IS ALREADY ON QUEST
        check = connection.execute(sqlalchemy.text(
            """
                SELECT * FROM quest_ledger
                WHERE char_id = :charID AND complete = False
                
            """), {'charID': charID})
        if(check.rowcount < 1): 
            connection.execute(sqlalchemy.text(
            """
                INSERT INTO game_log (error_id, char_id, description)
                VALUES (:errorID, :charID, :desc)
                
            """), {'errorID': 101,'charID': charID, 'desc': "CHARACTER HAS NO QUEST TO COMPLETE"})
            print("CHARACTER HAS NO QUEST")
            return "CHARACTER HAS NO QUEST"
        elif (check.rowcount > 1):
            connection.execute(sqlalchemy.text(
            """
                INSERT INTO game_log (error_id, char_id, description)
                VALUES (:errorID, :charID, :desc)
                
            """), {'errorID': 102,'charID': charID, 'desc': "CHARACTER HAS MULTIPLE QUESTS TO COMPLETE"})
            print("CHARACTER ON MORE THAN ONE QUEST")
            return "CHARACTER ON MORE THAN ONE QUEST"
        
        #UPDATE QUEST LEDGER
        result = connection.execute(sqlalchemy.text(
            """
                UPDATE quest_ledger
                SET complete = True
                WHERE char_id = :charID AND complete = False
                returning quest_id
                
            """), {'charID': charID}).scalar_one()
        connection.execute(sqlalchemy.text(
            """
                INSERT INTO game_log (error_id, char_id, description)
                VALUES (:errorID, :charID, :desc)
                
            """), {'errorID': 0,'charID': charID, 'desc': "CHARACTER COMPLETED CURRENT QUEST: " + str(result)})
    
    return {"success": True}