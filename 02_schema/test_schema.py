import requests
import pytest
from datetime import datetime

BASE_URL = "http://localhost:5000"
MODERATION_URL = "http://localhost:5001"
AUTH_HEADER = {"Authorization": "Bearer token-user-1"}

REVIEW_FIELDS = {"id", "book_id", "rating", "comment", "user_id", "timestamp"}
BOOK_FIELDS = {"id", "title", "author"}


@pytest.fixture(autouse=True)
def reset_moderation():
    yield
    requests.post(f"{MODERATION_URL}/admin/reset")


@pytest.fixture
def book():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Schema Book", "author": "Author"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


def post_review(book_id, rating=4, comment="Solid book"):
    return requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": rating, "comment": comment},
        headers=AUTH_HEADER,
    )


def assert_review_schema(review):
    assert set(review.keys()) == REVIEW_FIELDS
    assert isinstance(review["id"], str)
    assert isinstance(review["book_id"], str)
    assert isinstance(review["rating"], int)
    assert isinstance(review["comment"], str)
    assert isinstance(review["user_id"], str)
    assert isinstance(review["timestamp"], str)
    datetime.fromisoformat(review["timestamp"])


def assert_book_schema(book_body):
    assert set(book_body.keys()) == BOOK_FIELDS
    assert isinstance(book_body["id"], str)
    assert isinstance(book_body["title"], str)
    assert isinstance(book_body["author"], str)


def assert_error_schema(body):
    assert isinstance(body, dict)
    assert "error" in body
    assert isinstance(body["error"], str)


def test_post_review_has_exact_fields(book):
    resp = post_review(book["id"])
    assert_review_schema(resp.json())


def test_get_reviews_for_book_returns_array_with_matching_schema(book):
    post_review(book["id"])
    post_review(book["id"], rating=2, comment="Meh")
    resp = requests.get(f"{BASE_URL}/books/{book['id']}/reviews")
    body = resp.json()
    assert isinstance(body, list)
    for review in body:
        assert_review_schema(review)


def test_get_reviews_for_book_empty_list_before_any_review(book):
    resp = requests.get(f"{BASE_URL}/books/{book['id']}/reviews")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_all_reviews_returns_array_with_matching_schema(book):
    post_review(book["id"])
    resp = requests.get(f"{BASE_URL}/reviews")
    body = resp.json()
    assert isinstance(body, list)
    for review in body:
        assert_review_schema(review)


def test_put_review_schema_matches_post_schema(book):
    created = post_review(book["id"]).json()
    resp = requests.put(
        f"{BASE_URL}/books/{book['id']}/reviews/{created['id']}",
        json={"rating": 5, "comment": "Changed my mind"},
        headers=AUTH_HEADER,
    )
    assert_review_schema(resp.json())


def test_400_error_has_error_field(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"comment": "Missing rating"},
        headers=AUTH_HEADER,
    )
    assert resp.status_code == 400
    assert_error_schema(resp.json())


def test_404_error_has_error_field():
    resp = requests.get(f"{BASE_URL}/books/does-not-exist/reviews")
    assert resp.status_code == 404
    assert_error_schema(resp.json())


def test_422_error_has_error_field(book):
    resp = post_review(book["id"], rating=0)
    assert resp.status_code == 422
    assert_error_schema(resp.json())


def test_503_error_has_error_field(book):
    requests.post(f"{MODERATION_URL}/admin/configure", json={"mode": "error"})
    resp = post_review(book["id"])
    assert resp.status_code == 503
    assert_error_schema(resp.json())


def test_post_book_has_exact_fields():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Another Book", "author": "Someone"})
    body = resp.json()
    assert_book_schema(body)
    requests.delete(f"{BASE_URL}/books/{body['id']}")


def test_get_book_schema_matches_post_book_schema(book):
    resp = requests.get(f"{BASE_URL}/books/{book['id']}")
    assert_book_schema(resp.json())
