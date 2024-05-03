User Stories (12):
As a role-player, I want to create a character with unique characteristics, in order to be expressive and customize my play.

As a player who is easily bored, I want quests to play differently each time, so that I can get novel entertainment value from each play period.

As a player who likes rewards and words of affirmation, I want useful loot from quests, so that I can buy upgrades and feel accomplished.

As a gamer who values progression, I want a mechanism for my character to get stronger with gameplay, so that I can see the fruits of my labor and feel accomplished.

As a gamer who likes tiered upgrades, I want to be able to buy upgrades with my loot, so that harder quests become easier. 

As a busy player, I want to be able to quit the game and have my character’s progression saved when I come back, so that I don’t lose progress.

As a player, I want to view and manage my inventory of items, to keep track of what I have and can do in the game.

As a player who likes a challenge, I want to be able to choose between quests or paths of varying difficulty, so that I can test my luck or play it cool and easy.

As a player who needs to be visually engaged, I want the art for the quest to be varied and pretty, so that I can be excited and engaged with new quests.

As a player who can get tired of a game, I want the game to have built in waits for questing, so that I can keep coming back to the game.

As an admin who makes quests, I want a system of adding randomized or specified quest archetypes, so that I don’t have to make each quest manually for users.

As a player who wants to play more than once, I want to be able to reset my account progress and start over on a different path.

Exceptions (12):

Exception: Character is already on a quest

If the character is already on a quest and the player attempts to start another one, the game should prevent them from continuing citing that the character is already on a quest

Exception: Player attempts to add more inventory items than they have room for

Should the player not have enough room to fit all the inventory items they wish to add, the game should prevent them from doing so and ideally allow them to choose which items to discard until they can fit all of their items

Exception: Player attempts to buy gear without enough currency

Should the player not have enough currency to purchase the gear they are attempting to buy, the game should prevent them from buying the gear citing lack of funds

Exception: Player attempts to equip two of the same item

Should the player attempt to equip an item while they have already equipped an item of that type (ie. equipping a helmet while wearing a helmet), the game should ideally attempt to swap out the new helmet with the old one. Note: This may not apply to all equippable items.

Exception: Player attempts to name a character a name that is too long or only consists of blank characters

Should the player attempt to name a character a name that is too long or only consists of blank characters, the game should reject the name and give back an error to the user about the name violation.

Exception: Player attempts to access a quest that is too high level or, for whatever reason, does not meet the qualifications for

The game may have quests that require the player to meet a certain set of conditions before beginning. Should this happen, the game should reject the quest request and display an error to the user about what qualifications they lack.

Exception: Player attempts to access a quest that has since been invalidated

If we have a rotating set of quests for the player to embark on, we may encounter a problem where the player attempts to access a quest after it has been rotated out. This may be solved with an invalidating tag on all quest markers and should the player attempt to access an invalid quest, give back an error

Exception: Player attempts to access the same account on multiple instances

If a player attempts to play on the same account across multiple platforms at the same time, we log out all but the most recently used platform and display an error.

Exception: Player attempts to sell equipped gear

If the player attempts to sell gear that they have equipped, display an error that they must equip something else first

Exception: Player attempts to sell gear on a quest

If the player attempts to sell gear while they are on a quest, display an error that they must finish the quest in order to return to the shop where they can sell gear.

Exception: Player attempts to swap gear on a quest

If the player attempts to swap their gear while on a quest, display an error that tells them that gear cannot be swapped while on a quest

Exception: Player attempts to use a name already in use for their character

If the player attempts to give their character a name that is already in use, display an error and prompt them to choose a new name.
