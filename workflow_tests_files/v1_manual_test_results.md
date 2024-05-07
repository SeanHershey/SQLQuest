Example Flows #3: Player creates a character, but immediately regrets the name they gave their character and seeks to change it

A player by the name of Steve wants to create a new character, an adventurer by the name of Bloodfeather after his favorite band! So Steve goes to the character creator and inputs the character's name Bloodfeather and calls POST /character. This creates the character, and further API call /character/109/inventory (109 is Bloodfeather's character ID) will add the starting inventory. Steve is about to finalize, when he gets a notification on his Bloodfeather facebook group. The entire band has been exposed for hating SQL optimizations and random Taylor Swift trivia. This cannot stand. Steve can no longer support them. He deletes his facebook group, but now realizes he does not want a character named after a band that hates swift queries and queries about Swift. He goes to the rename form and inputs his character's new name, one that will bring justice to both. Steve then calls /character/rename to officially rename his character.

1. Create the character
curl -X 'POST' \
  'http://127.0.0.1:3000/character?name=Bloodfeather' \
  -H 'accept: application/json' \
  -d ''
Response: 3

  2. Add starting inventory
curl -X 'POST' \
  'http://127.0.0.1:3000/character/inventory?charID=3' \
  -H 'accept: application/json' \
  -d ''
Response: "OK"

  3. Renaming the character with /character/rename
  curl -X 'POST' \
  'http://127.0.0.1:3000/character/rename?charID=3&name=Francie' \
  -H 'accept: application/json' \
  -d ''
  Response: "OK"