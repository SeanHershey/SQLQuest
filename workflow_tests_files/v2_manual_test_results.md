#Example workflow
A player wants to see what items are in their characters inventory, and once checked they decide to equip their helmet to their character.


#Testing Results
Setup.
Follow v1_manual_test_flow.md to get a starter inventory to test on, for this test we got id 3.

Step 1. Get inventory
1. curl -X 'GET' \
  'http://127.0.0.1:3000/inventory/3' \
  -H 'accept: application/json'
2. 
[
  {
    "item_id": 1,
    "item_name": "Starter Sword",
    "quantity": 1,
    "equipped": false,
    "equip_slot": "Weapon"
  },
  {
    "item_id": 2,
    "item_name": "Starter Helmet",
    "quantity": 1,
    "equipped": false,
    "equip_slot": "Head"
  }
]

Step 2. Equip an item
1. curl -X 'POST' \
  'http://127.0.0.1:3000/equip/3/2' \
  -H 'accept: application/json' \
  -d ''
2.
{
  "success": true
}