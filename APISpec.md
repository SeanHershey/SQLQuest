# API Specification for SQL Quest



## 1.  Character Creation Flow

The API calls are made in this sequence when creating a character:
1. `Create base character`
2. `Rename character`
3. `Choose starter inventory`
4. `Finilize creation`

### 1.1 Create Base Character - `/character/` (POST)

Creates a base character that is new for the player.

**Response**:

```json
{
    "id": "string"
{
```

### 1.2 Rename Character - `/character/{char_id}/rename` (POST)

Renames a character.

**Response**:

```json
{
    "success": "boolean"
}
```

### 1.3 Choose Starter Inventory - `/character/{char_id}/inventory` (POST)

With a shop allow starter items to be asigned to a character.

**Response**:

```json
{
    "success": "boolean"
}
```



## 2.  Inventory

The API calls are made in this sequence when equipping an item on a character:

### 2.1 Get Inventory - `/inventory/{char_id}` (GET)

Using the character ID, open the inventory and returns a list of all items in the inventory
Note: Items are still subject to change

**Response**:

```json
[
    {
        "item_id": "integer",
        "item_name": "string", /* Unique to each item */
        "quantity": "integer", /* Non-negative */
        "equipped": "boolean", 
        "equip_slot": "string", /* Used to determine equipment conflicts */
    },
    ...
]
```

### 2.2 Post Inventory - `/equip/{char_id}/{item_id}` (POST)

Using the character ID and item ID, change an item's status to equipped
Note: Logic shoud be to de-equip an item if the item is in the same slot as the item requested

**Response**:

```json
{
    "success": "boolean"
}
```



## 3. Quests

The API calls are made in this sequence when sending a character on a quest:

### 3.1 Get Quest Board - `/quests` (GET)

Get a list of quests that the character can embark on

**Response**:

```json
[
    {
        "name": quest.name,
        "description": quest.description,
        "level": quest.level,
        "gold": quest.gold,
        "itemID": quest.item_id
    }
]
```

### 3.2 Get Character's Completed Quests - `/quests/character` (GET)

Get a list of quests that the character has completed

**Response**:

```json
[
    {
        "time_started": quest.created_at,
        "name": quest.name,
        "description": quest.description,
        "level": quest.level,
        "gold": quest.gold,
        "itemID": quest.item_id
    }
]
```

### 3.3 Begin Quest - `/quests/{char_id}/{quest_id}` (POST)

Write an entry to a new questing table (Relation between characters and quests)
to allow the character to begin embarking upon the quest chosen

**Response**:

```json
{
    "success": "boolean"
}
```

### 3.4 Complete Quest - `/quests/{char_id}/{quest_id}` (DELETE)

Remove an entry from the questing table and give the character rewards.
Note: This will be removing the questing entry, adding the gold reward, and adding the item reward
this must be done atomically, so I don't think we can separate this into 3 separate API calls

**Response**:

```json
{
    "success": "boolean"
}
```



## 4.  Shop

Shop api calls are made in this sequence after a quest

### 4.1 Get Shop Inventory - `/shop` (GET)

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

### 4.2 Buy Items - `/shop/` (POST)

The request json contains a list of entries containing item names and quantities. Returns true
if all items can be purchased and are successfully transferred to player inventory.

**Request**:

```json
{
    "success": "boolean"
}
```

**Response**:

```json
{
    "items_bought": "string",
    "gold_paid": "integer"
}
```

### 4.3 Stock a shop - `/shop/{shop_id}` (POST)

**Request**:

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

**Response**:

```json
{
    "success": "boolean"
}
```
