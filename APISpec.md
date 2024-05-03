# API Specification for SQL Quest

## 1.  Character creation flow

The API calls are made in this sequence when creating a character:
1. `Create base character`
2. `Rename character`
3. `Choose starter inventory`
4. `Finilize creation`

### 1.1 Create Base Character - `/character/` (POST)

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

### 1.4 Finilize Creation - `/character/{char_id}/create` (POST)

Locks the characters starter items and name in place so they can start on their quests.

**Response**:

```json
{
    "success": "boolean"
}
```



## 2.  

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
        "equipped": "integer", /* 0 if item is not equipped, >0 if item is equipped. Integer determines equip conflicts*/
    }
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




## 3.  

The API calls are made in this sequence when sending a character on a quest:

### 3.1 Get Quest Board - `/quests` (GET)

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

### 3.2 Character picks quest - `/quests/{char_id}/{quest_id}` (POST)

Write an entry to a new questing table (Relation between characters and quests)
to allow the character to begin embarking upon the quest chosen

**Response**:

```json
{
    "success": "boolean"
}
```

### 3.3 Character completes quest - `/quests/{char_id}/{quest_id}` (DELETE)

Remove an entry from the questing table and give the character rewards.
Note: This will be removing the questing entry, adding the gold reward, and adding the item reward
this must be done atomically, so I don't think we can separate this into 3 separate API calls

**Response**:

```json
{
    "success": "boolean"
}
```
## 4.  

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

### 4.2 Character buys items - `/shop/` (POST)

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





# API Specification for Potion Exchange Compatible Shops

## 1. Customer Purchasing

The API calls are made in this sequence when making a purchase:
1. `Get Catalog`
2. `Customer Visits`
3. `New Cart`
4. `Add Item to Cart` (Can be called multiple times)
5. `Checkout Cart`
6. `Search Orders`

### 1.1. Get Catalog - `/catalog/` (GET)

Retrieves the catalog of items. Each unique item combination should have only a single price. You can have at most 6 potion SKUs offered in your catalog at one time.

**Response**:

```json
[
    {
        "sku": "string", /* Matching regex ^[a-zA-Z0-9_]{1,20}$ */
        "name": "string",
        "quantity": "integer", /* Between 1 and 10000 */
        "price": "integer", /* Between 1 and 500 */
        "potion_type": [r, g, b, d] /* r, g, b, d are integers that add up to exactly 100 */
    }
]
```

### 1.2. Visits - `/carts/visits/{visit_id}` (POST)

Shares the customers that visited the store on that tick. Not all
customers end up purchasing because they may not like what they see
in the current catalog.

**Request**:

```json
[
  {
    "customer_name": "string",
    "character_class": "string",
    "level": "number"
  },
  {
    ...
  }
]
```
**Response**:

```json
{
    "success": "boolean"
}
```

### 1.3. New Cart - `/carts/` (POST)

Creates a new cart for a specific customer.

**Request**:

```json
{
  "customer_name": "string",
  "character_class": "string",
  "level": "number"
}
```

**Response**:

```json
{
    "cart_id": "string" /* This id will be used for future calls to add items and checkout */
}
``` 

### 1.4. Add Item to Cart - `/carts/{cart_id}/items/{item_sku}` (PUT)

Updates the quantity of a specific item in a cart. 

**Request**:

```json
{
  "quantity": "integer"
}
```

**Response**:

```json
{
    "success": "boolean"
}
```

### 1.5. Checkout Cart - `/carts/{cart_id}/checkout` (POST)

Handles the checkout process for a specific cart.

**Request**:

```json
{
  "payment": "string",
}
```

**Response**:

```json
{
    "total_potions_bought": "integer",
    "total_gold_paid": "integer"
}
```

### 1.6. Search orders - `/carts/search/` (GET)
Searches for orders based on specified query parameters.

**Query Parameters**:

- `customer_name` (optional): The name of the customer.
- `potion_sku` (optional): The SKU of the potion.
- `search_page` (optional): The page number of the search results.
- `sort_col` (optional): The column to sort the results by. Possible values: `customer_name`, `item_sku`, `line_item_total`, `timestamp`. Default: `timestamp`.
- `sort_order` (optional): The sort order of the results. Possible values: `asc` (ascending), `desc` (descending). Default: `desc`.

**Response**:

The API returns a JSON object with the following structure:

- `previous`: A string that represents the link to the previous page of results. If there is no previous page, this value is an empty string.
- `next`: A string that represents the link to the next page of results. If there is no next page, this value is an empty string.
- `results`: An array of objects, each representing a line item. Each line item object has the following properties:
    - `line_item_id`: An integer that represents the unique identifier of the line item.
    - `item_sku`: A string that represents the SKU of the item. This includes the quantity and the name of the item.
    - `customer_name`: A string that represents the name of the customer who purchased the item.
    - `line_item_total`: An integer that represents the total cost of the line item.
    - `timestamp`: A string that represents the date and time when the line item was created. This is in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).


## 2. Bottling

The API calls are made in this sequence when the bottler comes:
1. `Get Bottle Plan`
2. `Deliver Bottles`

### 2.1. Get Bottle Plan - `/bottler/plan` (POST)

Gets the plan for bottling potions.

**Response**:

```json
[
    {
        "potion_type": [r, g, b, d],
        "quantity": "integer"
    }
]
```

### 2.2. Deliver Bottles - `/bottler/deliver/{order_id}` (POST)

Posts delivery of potions. order_id is a unique value representing
a single delivery. 

**Request**:

```json
[
  {
    "potion_type": [r, g, b, d],
    "quantity": "integer"
  }
]
```

## 3. Barrel Purchases

The API calls are made in this sequence when Barrel Purchases can be made:
1. `Get Barrel Purchase Plan`
2. `Deliver Barrels`

### 3.1. Get Barrel Purchase Plan - `/barrels/plan` (POST)

Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
and the shop returns back which barrels they'd like to purchase and how many.

**Request**:

```json
[
  {
    "sku": "string",
    "ml_per_barrel": "integer",
    "potion_type": "integer",
    "price": "integer",
    "quantity": "integer"
  }
]
```

**Response**:

```json
[
    {
        "sku": "string", /* Must match a sku from the catalog just passed in this call */
        "quantity": "integer" /* A number between 1 and the quantity available for sale */
    }
]
```

### 3.2. Deliver Barrels - `/barrels/deliver/{order_id}` (POST)

Posts delivery of barrels. order_id is a unique value representing
a single delivery.

**Request**:

```json
[
  {
    "sku": "string",
    "ml_per_barrel": "integer",
    "potion_type": "integer",
    "price": "integer",
    "quantity": "integer"
  }
]
```

### 4. Admin Functions

### 4.1. Reset Shop - `/admin/reset` (POST)

A call to reset shop will delete all inventory and in-flight carts and reset gold back to 100. The
shop should take this as an opportunity to remove all of their inventory and set their gold back to
100 as well.

### 5. Info Functions

### .1. Current time - `/info/current_time` (POST)

Shares what the latest time (in game time) is. 

**Request**:

```json
[
  {
    "day": "string",
    "hour": "number"
  }
]
```

### 6. Audit Functions

### 6.1. Get Inventory Summary - `/inventory/audit` (GET)

Return a summary of your current number of potions, ml, and gold.

**Response**:
```json
{
  "number_of_potions": "number",
  "ml_in_barrels": "number",
  "gold": "number"
)
```  

### 6.2 Get capacity purchase plan - `/inventory/plan` (POST)

What additional potion or ML capacity the shop would like to buy. Called once a day.
You start with 1 capacity of potion and 1 capacity of ml storage. Each potion capacity
allows 50 potion storage. Each ml capacity allows 10k of ml storage.

**Response**:
```json
{
  "potion_capacity": "number",
  "ml_capacity": "number"
}
```

### 6.3 Deliver capacity purchased - `/inventory/deliver` (POST)

Delivers capacity purchased back to shop. Called when a capacity purchase succeeds.

**Request**:
```json
{
  "potion_capacity": "number",
  "ml_capacity": "number"
}
```
