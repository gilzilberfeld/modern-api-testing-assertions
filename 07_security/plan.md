# Round 7: Security

The auth model has two questions: authentication (who are you?) and authorization (what can you do?).

## Test plan

**Authentication:**
1. POST review with valid token → 201
2. POST review with no token → 401
3. POST review with invalid token → 401
4. PUT review with no token → 401
5. DELETE review with no token → 401

**Authorization — ownership:**
6. User A creates review, user B tries to edit → 403
7. User A creates review, user B tries to delete → 403
8. User A edits their own review → 200
9. User A deletes their own review → 204

**Public read access:**
10. GET /books/{bookId}/reviews without token → 200
11. GET /reviews without token → 200
