# Round 2: Schema

## What's missing from Round 1

- No test ever asserted the response has *exactly* these fields and no others
- No test checked the type of a field, only that it round-tripped correctly
- List endpoints were never checked for a consistent per-item schema
- Error responses were never checked for a consistent shape across status codes
- Nothing checked what an empty list endpoint returns before any data exists

## Test plan

**POST /books/{bookId}/reviews:**
1. Response has exactly the fields: id, book_id, rating, comment, user_id, timestamp — no more, no fewer
2. id and book_id are strings
3. rating is an integer
4. comment is a string
5. user_id is a string
6. timestamp is a string in valid ISO 8601 format

**GET /books/{bookId}/reviews:**
7. Response is a JSON array
8. Each item matches the same schema as the POST response
9. Before any review is created, the endpoint returns an empty array — not null, not a missing key

**GET /reviews:**
10. Response is a JSON array
11. Each item matches the same schema as the POST response

**PUT /books/{bookId}/reviews/{reviewId}:**
12. Response schema matches the POST response schema exactly

**Error responses (400, 404, 422, 503):**
13. Every error response is a JSON object with an "error" field
14. The "error" field is a string

**Books:**
15. POST /books response has exactly the fields: id, title, author
16. GET /books/{bookId} response has the same schema as the POST /books response
