# Round 2 Prompt

I have a bookstore API. There's a feature: "add a review to a book."

Endpoints:
- POST /books/{bookId}/reviews — body: {"rating": 1-5, "comment": "..."}
- GET /books/{bookId}/reviews — list reviews for a book
- GET /reviews — list all reviews across all books
- PUT /books/{bookId}/reviews/{reviewId} — edit a review
- DELETE /books/{bookId}/reviews/{reviewId} — delete a review

Auth: Authorization: Bearer <token>. Tokens: "token-user-1" → user-1, "token-user-2" → user-2.

Write pytest tests for the full "add a review" feature — not just the POST endpoint, but the entire workflow: creating reviews, verifying they appear in listing endpoints, editing them, deleting them. Include edge cases around non-existent resources and data isolation between books.
