#Example workflow
A player wants to trade their helmet for another players sword. They trade, and then try to submit the same trade again without the items they offered and the trade fails.


#Testing Results
Setup.
Follow v1_manual_test_flow.md twice to get two starter inventories to test on, for this test we got ids 4 and 5. Each with 1 unequipped instance of items 1 and 2.

Step 1. Perform Trade
1. curl -X 'POST' \
  'http://127.0.0.1:2000/inventory/3/trade/4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "offer": [
    {
      "item_id": 1,
      "quantity": 1
    }
  ],
  "request": [
    {
      "item_id": 2,
      "quantity": 1
    }
  ]
}'
2. 
{
    "success": true
}
Changes are reflected correctly in inventory and game log. Items with a resulting quantity of 0 were deleted.

Step 2. Attempt Trade again
1. curl -X 'POST' \
  'http://127.0.0.1:2000/inventory/3/trade/4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "offer": [
    {
      "item_id": 1,
      "quantity": 1
    }
  ],
  "request": [
    {
      "item_id": 2,
      "quantity": 1
    }
  ]
}'
2. {
    "success": false
}
Trade failure logged in game log. No changes to inventory.