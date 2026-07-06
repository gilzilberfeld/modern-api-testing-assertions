import random
from locust import HttpUser, task, between, events


class ReviewUser(HttpUser):
    wait_time = between(0.05, 0.2)
    book_id = None

    def on_start(self):
        resp = self.client.post(
            "/books",
            json={"title": "Load Test Book", "author": "Locust User"},
        )
        self.book_id = resp.json()["id"]

    @task(3)
    def post_review(self):
        self.client.post(
            f"/books/{self.book_id}/reviews",
            json={
                "rating": random.randint(1, 5),
                "comment": f"Load test review #{random.randint(1, 10000)}",
            },
            headers={"Authorization": "Bearer token-user-1"},
        )

    @task(1)
    def get_reviews(self):
        self.client.get(f"/books/{self.book_id}/reviews")


@events.quitting.add_listener
def assert_error_rate(environment, **kwargs):
    if environment.stats.total.fail_ratio > 0.01:
        environment.process_exit_code = 1
