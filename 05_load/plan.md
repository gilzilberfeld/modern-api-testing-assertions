# Round 5: Load

Load testing answers a different question: not "does it work" but "does it hold up."

## Test plan

**User behavior:**
- on_start: create one book per virtual user
- Task weight 3: POST /books/{bookId}/reviews with random rating and comment
- Task weight 1: GET /books/{bookId}/reviews

**Run parameters:**
- 100 concurrent users
- Ramp up: 10 users/second
- Duration: 30 seconds

**Metrics to watch:**
- Error rate: **pass/fail threshold < 1%** (enforced via exit code)
- Median response time: target < 500ms
- 95th percentile: watch for spikes
- Requests/second: sustained throughput

**Command:**
```
locust -f 05_load/locustfile.py --headless -u 100 -r 10 -t 30s --host http://localhost:5000
```
