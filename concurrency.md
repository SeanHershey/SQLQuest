# Concurrency Concerns and Fixes

## Begin 2 Quests at the same time
By having a character begin two different quests at the same time the check for if the character is already in a quest will pass for both requests. This causes the issue of being accepted to go on two or more quests at the same time which is an exploit and concurrency bug that we will have to handle. A way we can handle this is by locking the quest ledger before checking the character's quest status and inserting a new quest. 

## Equip 2 items at the same time
Our equip logic checks for inventory capacity but is vulnerable to two or more concurrent calls to equip different or the same items. One way we can fix this is by locking the inventory while equipping.

## Buy 2 items at the same time
When we buy 2 items at the same time the gold value of the player will not reflect this change as it is not currently a leger and the enough gold requirement check is vulnerable to concurrency issues which require locking when buying an item. 

Note: Sequence Diagrams Can Be Found At File: CSC365 Concurrency
