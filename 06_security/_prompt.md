# Round 6 Prompt

The bookstore API uses token-based auth. 

- Auth header: "Authorization: Bearer <token>"
- Valid tokens: "token-user-1" → user-1, "token-user-2" → user-2
- POST, PUT, DELETE /reviews require a valid token
- GET endpoints are public (no auth required)
- Only the review's author (matched by user_id from the token) can edit or delete their review

Write pytest tests verifying:
1. Authenticated users can create reviews
2. Unauthenticated requests to write endpoints return 401
3. Invalid tokens return 401
4. Cross-user access to edit/delete returns 403
5. Users can edit and delete their own reviews
6. Read endpoints work without auth
