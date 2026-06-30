import requests
import pytest
import concurrent.futures

BASE_URL = "http://localhost:5000"
THREAD_COUNT = 10


@pytest.fixture
def book():
    resp = requests.post(f"{BASE_URL}/books", json={"title": "Concurrency Book", "author": "Thread Author"})
    b = resp.json()
    yield b
    requests.delete(f"{BASE_URL}/books/{b['id']}")


def submit_review(book_id, index):
    return requests.post(
        f"{BASE_URL}/books/{book_id}/reviews",
        json={"rating": (index % 5) + 1, "comment": f"Concurrent review {index}"},
        headers={"Authorization": f"Bearer token-user-{(index % 3) + 1}"},
    )


def test_all_concurrent_submissions_succeed(book):
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = [executor.submit(submit_review, book["id"], i) for i in range(THREAD_COUNT)]
        responses = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert all(r.status_code == 201 for r in responses)


def test_all_reviews_are_saved(book):
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = [executor.submit(submit_review, book["id"], i) for i in range(THREAD_COUNT)]
        concurrent.futures.wait(futures)

    reviews = requests.get(f"{BASE_URL}/books/{book['id']}/reviews").json()
    assert len(reviews) == THREAD_COUNT


def test_no_duplicate_review_ids(book):
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = [executor.submit(submit_review, book["id"], i) for i in range(THREAD_COUNT)]
        responses = [f.result() for f in concurrent.futures.as_completed(futures)]

    ids = [r.json()["id"] for r in responses]
    assert len(ids) == len(set(ids))


def test_each_review_has_correct_data(book):
    submissions = [
        {"rating": (i % 5) + 1, "comment": f"Concurrent review {i}"}
        for i in range(THREAD_COUNT)
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = [
            executor.submit(
                requests.post,
                f"{BASE_URL}/books/{book['id']}/reviews",
                **{
                    "json": submissions[i],
                    "headers": {"Authorization": f"Bearer token-user-{(i % 3) + 1}"},
                },
            )
            for i in range(THREAD_COUNT)
        ]
        responses = [f.result() for f in futures]

    for i, resp in enumerate(responses):
        body = resp.json()
        assert body["rating"] == submissions[i]["rating"]
        assert body["comment"] == submissions[i]["comment"]
