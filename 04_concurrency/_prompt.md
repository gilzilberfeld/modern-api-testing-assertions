# Round 4 Prompt

The bookstore API uses an in-memory store with a threading.Lock() for concurrent access. The Flask server runs in threaded mode.

Write a pytest test that submits 10 reviews simultaneously to the same book using concurrent.futures.ThreadPoolExecutor. Verify:
- All 10 submissions succeed (201)
- All 10 reviews appear in GET /books/{bookId}/reviews
- No duplicate review IDs
- Each review's rating and comment match what was submitted

Auth header: "Authorization: Bearer token-user-{N}" for users 1-3.
