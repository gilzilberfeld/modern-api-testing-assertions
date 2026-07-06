# Round 4 Prompt

The POST /books/{bookId}/reviews endpoint calls an external moderation service before saving. The server has a 3-second timeout on that call. Possible outcomes:
- Moderation approves → review saved, 201
- Moderation rejects → 422 with reason, review NOT saved
- Moderation returns 500 → 503, review NOT saved
- Moderation times out → 504, review NOT saved
- Moderation unreachable → 503, review NOT saved

The moderation service (http://localhost:5001) has admin endpoints for test control:
- POST /admin/configure — body: {"mode": "approve"|"reject"|"error"|"delay", "delay_seconds": N, "reject_reason": "..."}
- POST /admin/reset — restores default (approve) behavior

Write a test plan covering:
1. Each moderation failure mode and its impact on the response code and whether the review is saved
2. System health after a moderation failure
3. Malformed and edge-case inputs (bad JSON, wrong content type, large payloads, special characters)
