import requests
import pytest

BASE_URL = "http://localhost:5000"
MODERATION_URL = "http://localhost:5001"
AUTH_HEADER = {"Authorization": "Bearer token-user-1"}


@pytest.fixture(autouse=True)
def reset_moderation():
    yield
    requests.post(f"{MODERATION_URL}/admin/reset")


@pytest.fixture
def book():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Structural Book", "author": "Author"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


def mock_moderation(config):
    requests.post(f"{MODERATION_URL}/admin/configure", json=config)


def post_review(book_id, comment="Normal review", rating=4):
    return requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": rating, "comment": comment},
        headers=AUTH_HEADER,
    )


def test_moderation_rejection_returns_422_and_reason(book):
    mock_moderation({"mode": "reject", "reject_reason": "Offensive language"})
    resp = post_review(book["id"])
    assert resp.status_code == 422
    assert "Offensive language" in resp.json().get("reason", "")


def test_rejected_review_is_not_saved(book):
    mock_moderation({"mode": "reject"})
    post_review(book["id"])
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert len(reviews) == 0


def test_moderation_error_returns_503(book):
    mock_moderation({"mode": "error"})
    resp = post_review(book["id"])
    assert resp.status_code == 503


def test_moderation_error_review_not_saved(book):
    mock_moderation({"mode": "error"})
    post_review(book["id"])
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert len(reviews) == 0


def test_moderation_timeout_returns_504(book):
    mock_moderation({"mode": "delay", "delay_seconds": 5})
    resp = post_review(book["id"])
    assert resp.status_code == 504


def test_moderation_timeout_review_not_saved(book):
    mock_moderation({"mode": "delay", "delay_seconds": 5})
    post_review(book["id"])
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert len(reviews) == 0


def test_system_healthy_after_moderation_failure(book):
    mock_moderation({"mode": "error"})
    post_review(book["id"], comment="Will fail")
    requests.post(f"{MODERATION_URL}/admin/reset")

    resp = post_review(book["id"], comment="Should succeed")
    assert resp.status_code == 201
    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert len(reviews) == 1
    assert reviews[0]["comment"] == "Should succeed"


def test_malformed_json_returns_400(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        data="not json at all",
        headers={**AUTH_HEADER, "Content-Type": "application/json"},
    )
    assert resp.status_code == 400


def test_wrong_content_type_returns_400(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        data="rating=4&comment=test",
        headers={**AUTH_HEADER, "Content-Type": "text/plain"},
    )
    assert resp.status_code == 400


def test_extra_fields_handled_gracefully(book):
    resp = requests.post(
        f"{BASE_URL}/books/{book['id']}/reviews",
        json={"rating": 4, "comment": "Fine", "injected_field": "hacked"},
        headers=AUTH_HEADER,
    )
    assert resp.status_code in (200, 201, 400, 422)
    assert resp.status_code != 500


def test_large_payload_handled_gracefully(book):
    large_comment = "A" * 100_000
    resp = post_review(book["id"], comment=large_comment)
    assert resp.status_code != 500


def test_unicode_characters_stored_correctly(book):
    comment = "Ótimo livro! 书很好 🌟 Привет مرحبا"
    resp = post_review(book["id"], comment=comment)
    assert resp.status_code == 201
    assert resp.json()["comment"] == comment


def test_html_tags_stored_as_is(book):
    comment = "<script>alert('xss')</script>"
    resp = post_review(book["id"], comment=comment)
    assert resp.status_code == 201
    assert resp.json()["comment"] == comment


def test_sql_injection_string_stored_correctly(book):
    comment = "'; DROP TABLE reviews; --"
    resp = post_review(book["id"], comment=comment)
    assert resp.status_code == 201
    assert resp.json()["comment"] == comment
