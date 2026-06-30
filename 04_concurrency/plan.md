# Round 4: Concurrency

The store uses threading.Lock() — but does it actually hold up under concurrent load?

## Test plan

1. Submit 10 reviews simultaneously to the same book using ThreadPoolExecutor
2. All 10 responses return 201
3. GET /books/{bookId}/reviews returns exactly 10 reviews
4. No duplicate review IDs (the counter + lock must be atomic)
5. Each review's rating and comment match the corresponding submission (no data mixing)
