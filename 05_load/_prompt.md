# Round 5 Prompt

Write a Locust load test for the bookstore review API.

Setup: create a book in on_start (one per user). Then:
- Heavily hammer POST /books/{bookId}/reviews with randomized ratings (1-5) and comments
- Periodically hit GET /books/{bookId}/reviews for read load

Auth header: "Authorization: Bearer token-user-1"

The file should work with:
  locust -f 05_load/locustfile.py --headless -u 100 -r 10 -t 30s --host http://localhost:5000
