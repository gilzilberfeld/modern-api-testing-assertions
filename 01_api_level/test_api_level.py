import requests
import pytest
from datetime import datetime

BASE_URL = "http://localhost:5000"
AUTH_HEADER = {"Authorization": "Bearer token-user-1"}


@pytest.fixture
def book():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Test Book", "author": "Test Author"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


def post_review(book_id, rating=4, comment="Good book"):
    return requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": rating, "comment": comment},
        headers=AUTH_HEADER,
    )


def test_response_contains_all_fields(book):
    book_id = book["id"]
    resp = requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": 4, "comment": "Good book"},
        headers=AUTH_HEADER,
    )
    assert resp.status_code == 201
    body = resp.json()
    assert "id" in body
    assert "rating" in body
    assert "comment" in body
    assert "user_id" in body
    assert "timestamp" in body


def test_response_values_match_input(book):
    resp = post_review(book["id"], rating=3, comment="Decent read")
    body = resp.json()
    assert body["rating"] == 3
    assert body["comment"] == "Decent read"


def test_user_id_matches_authenticated_user(book):
    resp = post_review(book["id"])
    assert resp.json()["user_id"] == "user-1"


def test_id_is_nonempty_string(book):
    resp = post_review(book["id"])
    body = resp.json()
    assert isinstance(body["id"], str)
    assert len(body["id"]) > 0


def test_timestamp_is_valid_iso8601(book):
    resp = post_review(book["id"])
    timestamp = resp.json()["timestamp"]
    datetime.fromisoformat(timestamp)


def test_missing_rating_returns_400(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"comment": "Great!"},
        headers=AUTH_HEADER,
    )
    assert resp.status_code == 400


def test_missing_comment_returns_400(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": 4},
        headers=AUTH_HEADER,
    )
    assert resp.status_code == 400


def test_rating_zero_returns_422(book):
    resp = post_review(book["id"], rating=0)
    assert resp.status_code == 422


def test_rating_six_returns_422(book):
    resp = post_review(book["id"], rating=6)
    assert resp.status_code == 422


def test_rating_negative_returns_422(book):
    resp = post_review(book["id"], rating=-1)
    assert resp.status_code == 422


def test_rating_string_returns_422(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": "five", "comment": "Nice"},
        headers=AUTH_HEADER,
    )
    assert resp.status_code == 422


def test_empty_comment_is_accepted(book):
    resp = post_review(book["id"], comment="")
    assert resp.status_code == 201
    assert resp.json()["comment"] == ""


def test_review_ids_are_unique(book):
    ids = [post_review(book["id"]).json()["id"] for _ in range(5)]
    assert len(ids) == len(set(ids))
