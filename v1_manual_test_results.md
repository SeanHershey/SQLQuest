# Example workflow

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

# Testing results

54.156.210.47:0 - "POST /character/ HTTP/1.1" 200 OK
