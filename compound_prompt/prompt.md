# Compound Prompt

Before generating tests, answer these questions about the system under test, then generate a test plan covering each dimension below.

**Questions to answer first:**
1. What does this API do? What is the core feature being tested?
2. What endpoints are involved in the full workflow?
3. What external dependencies does the system have, and how can they fail?
4. What are the authentication and authorization rules?
5. What data invariants should hold across concurrent requests?
6. What scenarios require infrastructure beyond a running server to test?

---

## System context

Bookstore review API. POST /books/{bookId}/reviews creates a review. The server calls an external moderation service (localhost:5001) before saving. Auth: "Authorization: Bearer <token>" — valid tokens: "token-user-1" → user-1, "token-user-2" → user-2. Only the review's author can edit or delete their review. GET endpoints are public. The server has a 3-second timeout on moderation calls.

Moderation service admin endpoints:
- POST /admin/configure — body: {"mode": "approve"|"reject"|"error"|"delay", "delay_seconds": N, "reject_reason": "..."}
- POST /admin/reset

---

## Dimension 1: Feature Level

Test the full "add a review" workflow across all endpoints. Verify reviews appear in listing endpoints after creation, edits are reflected everywhere, deletes remove the data, and reviews don't leak between books.

## Dimension 2: Structural — Moderation Dependency

Test each moderation failure mode and verify:
- Rejected review: 422 with reason, review NOT saved
- Moderation 500: server returns 503, review NOT saved
- Moderation timeout (delay > 3s): server returns 504, review NOT saved
- System healthy after failure: next approved review saves correctly

Also test input edge cases: malformed JSON, wrong content type, large payloads, unicode, HTML, SQL injection strings.

## Dimension 3: Concurrency

Submit 10 reviews simultaneously using ThreadPoolExecutor. Verify: all succeed (201), all appear in GET, no duplicate IDs, each review's data matches its submission.

## Dimension 4: Load

Write a Locust file. Create a book in on_start. Task mix: 3x POST reviews (randomized data), 1x GET reviews. Target: 100 users, 10/s ramp, 30s run.

## Dimension 5: Security

Test auth model: no token → 401, invalid token → 401, wrong user edits → 403, owner edits → 200, owner deletes → 204, GET endpoints need no auth.

## Dimension 6: Reliability (plan only)

List the scenarios you cannot automate today: persistence after restart, geographic consistency, failover, backup/restore, timestamp accuracy, deterministic ordering. Explain what infrastructure each would require.
