import requests
import pytest

BASE_URL = "http://localhost:5000"
USER1 = {"Authorization": "Bearer token-user-1"}
USER2 = {"Authorization": "Bearer token-user-2"}


@pytest.fixture
def book():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Feature Book", "author": "Author A"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


@pytest.fixture
def book2():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Other Book", "author": "Author B"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


def add_review(book_id, rating=4, comment="Good", headers=None):
    return requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": rating, "comment": comment},
        headers=headers or USER1,
    ).json()


def test_created_review_appears_in_book_list(book):
    review = add_review(book["id"], comment="Great chapter")
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    ids = [r["id"] for r in reviews]
    assert review["id"] in ids


def test_created_review_appears_in_all_reviews(book):
    review = add_review(book["id"], comment="Loved it")
    all_reviews = requests.get(f"{BASE_URL}/reviews").json()
    ids = [r["id"] for r in all_reviews]
    assert review["id"] in ids


def test_multiple_reviews_all_present(book):
    r1 = add_review(book["id"], comment="First")
    r2 = add_review(book["id"], comment="Second")
    r3 = add_review(book["id"], comment="Third")
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    ids = {r["id"] for r in reviews}
    assert {r1["id"], r2["id"], r3["id"]}.issubset(ids)


def test_edit_review_reflected_in_book_list(book):
    review = add_review(book["id"], rating=3, comment="Okay")
    requests.put(
        f"{BASE_URL}/books/{book['id']}/reviews/{review['id']}",
        json={"rating": 5, "comment": "Actually great"},
        headers=USER1,
    )
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    updated = next(r for r in reviews if r["id"] == review["id"])
    assert updated["rating"] == 5
    assert updated["comment"] == "Actually great"


def test_edit_review_reflected_in_all_reviews(book):
    review = add_review(book["id"], comment="Meh")
    requests.put(
        f"{BASE_URL}/books/{book['id']}/reviews/{review['id']}",
        json={"comment": "Changed my mind"},
        headers=USER1,
    )
    all_reviews = requests.get(f"{BASE_URL}/reviews").json()
    updated = next(r for r in all_reviews if r["id"] == review["id"])
    assert updated["comment"] == "Changed my mind"


def test_delete_review_removed_from_book_list(book):
    review = add_review(book["id"], comment="To be deleted")
    requests.delete(f"{BASE_URL}/books/{book['id']}/reviews/{review['id']}", headers=USER1)
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert review["id"] not in [r["id"] for r in reviews]


def test_delete_review_removed_from_all_reviews(book):
    review = add_review(book["id"], comment="Also gone")
    requests.delete(f"{BASE_URL}/books/{book['id']}/reviews/{review['id']}", headers=USER1)
    all_reviews = requests.get(f"{BASE_URL}/reviews").json()
    assert review["id"] not in [r["id"] for r in all_reviews]


def test_post_to_nonexistent_book_returns_404():
    resp = requests.post(
        f"{BASE_URL}/books/nonexistent-999/reviews",
        json={"rating": 4, "comment": "Ghost book"},
        headers=USER1,
    )
    assert resp.status_code == 404


def test_put_nonexistent_review_returns_404(book):
    resp = requests.put(
        f"{BASE_URL}/books/{book['id']}/reviews/nonexistent-999",
        json={"rating": 5, "comment": "Nope"},
        headers=USER1,
    )
    assert resp.status_code == 404


def test_delete_nonexistent_review_returns_404(book):
    resp = requests.delete(
        f"{BASE_URL}/books/{book['id']}/reviews/nonexistent-999",
        headers=USER1,
    )
    assert resp.status_code == 404


def test_review_isolation_between_books(book, book2):
    review = add_review(book["id"], comment="Only for book A")
    reviews_b = requests.get(f"{BASE_URL}/books/{book2['id']}/reviews").json()
    assert review["id"] not in [r["id"] for r in reviews_b]
