Fake Data Modeling
Link to python file: https://github.com/Proefey/SQLQuestPopulate/blob/main/pop.py

Number of rows per Table:
characters = 70k
Inventory = 700k
Items = 1k
Quest_ledger = 350k
Quests = 1k
Shops = 1k
Stock = 10k

Note: Users and gamelog tables are not in use in the endpoints (The former being an abandoned idea, the latter being more of a debugging idea)

Justification of Numbers:
Items, Quests, Shops would reasonably not scale with user size. These are meant to be constant throughout the user’s experience (And thus hardcoded values). For the sake of testing we will assume 1k rows of each.

Stock is also something that does not scale with user size, but rather with the size of shops table. Therefore, we assume each shop holds on average 10 items for 10k rows

We will assume around 70k characters have been created as the game is somewhat popular. This is the basis for the other 2 tables.

For inventory and quest_ledger, we will assume each character has on average 10 items and has completed (Or is in the progress of completing) 5 quests.

In total, we would have 1.133 million rows in the database. This took a total time of 15 minutes and 30 seconds to insert, likely because I put the insert statements in a for loop. Since I would only have to do this one, I didn’t see a reason to complicate this (And I wasted 2 hours trying to optimize it)

Performance results of hitting endpoints
Here is the results of the 4 slowest endpoints

Get Inventory:
Planning Time: 0.531 ms
Execution Time: 22.556 ms

Equip Item (No conflict): 
Planning Time: 0.509 ms + 0.317ms + 0.634 ms + 0.210ms = 1.67ms
Execution Time: 29.814 ms + 0.137ms + 23.106 ms + 50.007ms = 0.1 seconds

Equip Item (Conflict):
Planning Time: 0.509 ms + 0.317ms + 0.634 ms + 0.210ms + 0.210ms = 1.88ms
Execution Time: 29.814 ms + 0.137ms + 23.106 ms + 50.007ms + 50.007ms = 0.15 seconds

Note: In cases of a conflict, an extra query must be made to unequip the item found. This is effectively the same query as the query that equips the item.

Trade: 
Planning Time: 0.209ms * 2 + 0.244ms * 2 + 0.190ms * 2 + 0.184ms * 2 + 0.190ms * 2 = 2.034 ms
Execution Time: 20.113ms * 2 + 24.388ms * 2 + 53.842ms * 2 + 24.087ms * 2 + 53.842ms * 2 = 0.352 seconds

Note: Because this is a 2-way trade, the queries are ran twice and the 3rd and 5th query are effectively the same in the worse case scenario

Get Character Quest History: 
Planning Time: 1.452 ms
Execution Time: 18.260 ms

Endpoints such as equip item, trade, get inventory, and get character quest history are the slowest. These endpoints are reading from records that have either 700k rows (Inventory) or 350k rows (Quest_ledger) and there is no indexing. 
Performance tuning
Our performance testing has shown us that the endpoints equip item, trade, get inventory, and get character quest history were the slowest, as these have either complex logic (In the case of the former 2) or simply must filter through the largest 2 tables in the database (In the case of all 4)

Get Inventory:
CREATE INDEX t2 ON inventory (char_id);
Planning Time: 0.368 ms
Execution Time: 1.149 ms

Equip Item (No conflict): 
CREATE INDEX t3 ON inventory (char_id, item_id);
Planning Time: 0.509 ms + 0.225ms + 0.274 ms + 0.662ms = 1.67ms
Execution Time: 0.197 ms + 0.093ms + 0.271 ms + 0.220ms = 0.781ms

Equip Item (Conflict):
Planning Time: 0.509 ms + 0.225ms + 0.274 ms + 0.662ms + 0.662ms = 2.3ms
Execution Time: 0.197 ms + 0.093ms + 0.271 ms + 0.220ms + 0.220ms = 1.001ms

Trade: 
CREATE INDEX t3 ON inventory (char_id, item_id);
Planning Time: 0.205ms * 2 + 0.292ms * 2 + 0.305ms * 2 + 0.261ms * 2 + 0.305ms * 2 = 2.736ms
Execution Time: 0.099ms * 2 + 0.105ms * 2 + 0.3ms * 2 + 0.106ms * 2 + 0.3ms*2 = 1.82ms

Get Character Quest History WITH Index: 
CREATE INDEX t1 ON quest_ledger (char_id);
Planning Time: 0.979 ms
Execution Time: 1.234 ms
