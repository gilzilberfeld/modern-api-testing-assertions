# Round 2: Feature Level

The feature isn't just POST /reviews. The feature is "add a review to a book." That involves multiple endpoints working together correctly.

## What's missing from Round 1

Round 1 tested the POST endpoint in isolation. We never verified:
- The review actually appears when you list reviews
- Edits are reflected in listing endpoints
- Deletes actually remove the data
- Data is isolated between books

## Test plan

**Create and read:**
1. Create review → appears in GET /books/{bookId}/reviews
2. Create review → appears in GET /reviews (all reviews)
3. Multiple reviews on same book → all present, count is correct

**Edit:**
4. PUT review → GET /books/{bookId}/reviews shows new data, old data gone
5. PUT review → GET /reviews shows new data

**Delete:**
6. DELETE review → gone from GET /books/{bookId}/reviews
7. DELETE review → gone from GET /reviews

**Error cases:**
8. POST to non-existent book → 404
9. PUT non-existent review → 404
10. DELETE non-existent review → 404

**Isolation:**
11. Review on book A does not appear in book B's review list
