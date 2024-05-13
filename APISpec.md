# API Specification for SQL Quest


## 1.  User creation flow

The API calls are made in this sequence when creating a character:
1. `Create User Account`

### 1.1 Create User Account - `/user/` (POST)

Creates a user account that is new for the player.

**Response**:

```json
{
    "success": "boolean"
}
```


## 2.  Character creation flow

The API calls are made in this sequence when creating a character:
1. `Create base character`
2. `Rename character`
3. `Choose starter inventory`
4. `Finilize creation`

### 2.1 Create Base Character - `/character/` (POST)

Creates a base character that is new for the player.

**Response**:

```json
[
    {
        "id": "string", /* Matching regex ^[a-zA-Z0-9_]{1,20}$ */
        "name": "string",
        "player_name": "string", /* Unique to each player */
        "gold": "integer",
        "inventory_id": "integer", /* refrence to an inventory */
        "quest_id": "boolean", /* reference to if the character is currently on a quest */
    }
]
```

### 2.2 Rename Character - `/character/{char_id}/rename` (POST)

Renames a character.

**Response**:

```json
{
    "success": "boolean"
}
```

### 2.3 Choose Starter Inventory - `/character/{char_id}/inventory` (POST)

With a shop allow starter items to be asigned to a character.

**Response**:

```json
{
    "success": "boolean"
}
```

### 2.4 Finilize Creation - `/character/{char_id}/create` (POST)

Locks the characters starter items and name in place so they can start on their quests.

**Response**:

```json
{
    "success": "boolean"
}
```



## 3.  

The API calls are made in this sequence when equipping an item on a character:

### 3.1 Get Inventory - `/inventory/{char_id}` (GET)

Using the character ID, open the inventory and returns a list of all items in the inventory
Note: Items are still subject to change

**Response**:

```json
[
    {
        "item_id": "integer",
        "item_name": "string", /* Unique to each item */
        "quantity": "integer", /* Non-negative */
        "equipped": "integer", /* 0 if item is not equipped, >0 if item is equipped. Integer determines equip conflicts*/
    }
]
```

### 3.2 Post Inventory - `/equip/{char_id}/{item_id}` (POST)

Using the character ID and item ID, change an item's status to equipped
Note: Logic shoud be to de-equip an item if the item is in the same slot as the item requested

**Response**:

```json
{
    "success": "boolean"
}
```




## 4.  

The API calls are made in this sequence when sending a character on a quest:

### 4.1 Get Quest Board - `/quests` (GET)

Get a list of quests that the character can embark on
Note: I am not entirely sure how to handle multiple items being given as a reward

**Response**:

```json
[
    {
        "quest_id": "integer",
        "quest_name": "string",
        "quest_reward_gold": "integer",
        "quest_item_reward_id": "integer", /* Reference to an item */
        "quest_duration_min": "integer",
        "quest_level_restriction": "integer",
    }
]
```

### 4.2 Character picks quest - `/quests/{char_id}/{quest_id}` (POST)

Write an entry to a new questing table (Relation between characters and quests)
to allow the character to begin embarking upon the quest chosen

**Response**:

```json
{
    "success": "boolean"
}
```

### 4.3 Character completes quest - `/quests/{char_id}/{quest_id}` (DELETE)

Remove an entry from the questing table and give the character rewards.
Note: This will be removing the questing entry, adding the gold reward, and adding the item reward
this must be done atomically, so I don't think we can separate this into 3 separate API calls

**Response**:

```json
{
    "success": "boolean"
}
```
## 5.  

Shop api calls are made in this sequence after a quest

### 5.1 Get Shop Inventory - `/shop` (GET)

Get the shop inventory, which contains item names, prices, and how many are available.

**Response**:

```json
[
    {
        "item_id": "integer",
        "item_name": "string",
        "quantity": "integer",
        "price": "integer",
    }
]
```

### 5.2 Character buys items - `/shop/` (POST)

The request json contains a list of entries containing item names and quantities. Returns true
if all items can be purchased and are successfully transferred to player inventory.

**Request**:

```json
{
    "item_name": "string",
    "quantity": "integer"
}
```

**Response**:

```json
{
    "success": "boolean"
}
```
