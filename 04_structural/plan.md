# Round 4: Structural

## What's missing from Round 3

Round 3 tested the happy path and basic error cases. It assumed:
- The moderation service always approves
- Clients always send well-formed JSON

Neither assumption holds in production.

## Test plan

**Moderation dependency:**
1. Moderation rejects → 422 returned, rejection reason in body, review NOT saved
2. Moderation returns 500 → server returns 503, review NOT saved
3. Moderation configured to delay beyond server timeout (>3s) → server returns 504, review NOT saved
4. After moderation failure, system is still healthy (next approved review saves successfully)

**Input edge cases:**
5. Malformed JSON body → 400
6. Wrong Content-Type (text/plain) → 400
7. Extra unexpected fields in body → handled gracefully (not a 500)
8. Extremely large comment payload → graceful response (not a 500)
9. Unicode characters in comment → stored and returned correctly
10. HTML tags in comment → stored and returned correctly (no sanitization)
11. SQL injection string in comment → stored and returned correctly
