import requests

BASE_URL = "http://localhost:5000"
AUTH_HEADER = {"Authorization": "Bearer token-user-1"}


def test_add_review():
    book = requests.post(f"{BASE_URL}/books", json={"title": "Clean Code", "author": "Robert Martin"}).json()

    response = requests.get(f"{BASE_URL}/books/{book['id']}")
    assert response.status_code == 200

    review_data = {
        "rating": 5,
        "comment": "Excellent book on software craftsmanship!",
        "user_id": "user-1",
    }
    response = requests.post(f"{BASE_URL}/books/{book['id']}/reviews", json=review_data, headers=AUTH_HEADER)
    assert response.status_code == 201

    requests.delete(f"{BASE_URL}/books/{book['id']}")
