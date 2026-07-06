import requests
import pytest

BASE_URL = "http://localhost:5000"
USER1 = {"Authorization": "Bearer token-user-1"}
USER2 = {"Authorization": "Bearer token-user-2"}
INVALID = {"Authorization": "Bearer not-a-real-token"}


@pytest.fixture
def book():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Security Book", "author": "Author"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


@pytest.fixture
def user1_review(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": 4, "comment": "User 1 review"},
        headers=USER1,
    )
    return {"book_id": book["id"], "review": resp.json()}


def test_authenticated_user_can_create_review(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": 5, "comment": "Authenticated"},
        headers=USER1,
    )
    assert resp.status_code == 201


def test_no_token_on_post_returns_401(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": 4, "comment": "No token"},
    )
    assert resp.status_code == 401


def test_invalid_token_on_post_returns_401(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": 4, "comment": "Bad token"},
        headers=INVALID,
    )
    assert resp.status_code == 401


def test_no_token_on_put_returns_401(user1_review):
    resp = requests.put(
        f"{BASE_URL}/books/{user1_review['book_id']}/reviews/{user1_review['review']['id']}",
        json={"comment": "Sneaky edit"},
    )
    assert resp.status_code == 401


def test_no_token_on_delete_returns_401(user1_review):
    resp = requests.delete(
        f"{BASE_URL}/books/{user1_review['book_id']}/reviews/{user1_review['review']['id']}"
    )
    assert resp.status_code == 401


def test_different_user_cannot_edit_review(user1_review):
    resp = requests.put(
        f"{BASE_URL}/books/{user1_review['book_id']}/reviews/{user1_review['review']['id']}",
        json={"comment": "User 2 takeover"},
        headers=USER2,
    )
    assert resp.status_code == 403


def test_different_user_cannot_delete_review(user1_review):
    resp = requests.delete(
        f"{BASE_URL}/books/{user1_review['book_id']}/reviews/{user1_review['review']['id']}",
        headers=USER2,
    )
    assert resp.status_code == 403


def test_user_can_edit_own_review(user1_review):
    resp = requests.put(
        f"{BASE_URL}/books/{user1_review['book_id']}/reviews/{user1_review['review']['id']}",
        json={"rating": 2, "comment": "Changed my mind"},
        headers=USER1,
    )
    assert resp.status_code == 200
    assert resp.json()["comment"] == "Changed my mind"


def test_user_can_delete_own_review(user1_review):
    resp = requests.delete(
        f"{BASE_URL}/books/{user1_review['book_id']}/reviews/{user1_review['review']['id']}",
        headers=USER1,
    )
    assert resp.status_code == 204


def test_get_reviews_is_public(book):
    resp = requests.get(f"{BASE_URL}/books/{book['id']}/reviews")
    assert resp.status_code == 200


def test_get_all_reviews_is_public():
    resp = requests.get(f"{BASE_URL}/reviews")
    assert resp.status_code == 200
