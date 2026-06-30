# Round 1: API Level

## What's missing
- Does the response body contain all expected fields?
- Do the values match what was sent?
- Are generated fields (id, timestamp) in the right format?
- Does the server reject invalid input?
- Are IDs unique?

## Test plan
1. Response body contains all required fields: id, rating, comment, user_id, timestamp
2. rating and comment in response match the submitted values
3. user_id in response matches the authenticated user
4. id is a non-empty string
5. timestamp is a valid ISO 8601 datetime string
6. Missing rating → 400
7. Missing comment → 400
8. rating = 0 → 422
9. rating = 6 → 422
10. rating = -1 → 422
11. rating = "five" (string) → 422
12. Empty string comment → accepted, stored as-is
13. Five reviews produce five distinct IDs
