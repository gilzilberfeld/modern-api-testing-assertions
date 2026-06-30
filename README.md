# Modern API Testing: Assertions You Can Trust

Example project for the W3 Webinar (July 15, 2026) by Gil Zilberfeld (TestinGil).

This is not a production application. It exists to demonstrate a progression from shallow API tests to tests that actually prove business logic works.

---

## What's here

| Folder | What it shows |
|--------|--------------|
| `00_green_mirage/` | A test that passes and proves nothing |
| `01_api_level/` | Testing the response body, not just the status code |
| `02_feature_level/` | Testing the full workflow across multiple endpoints |
| `03_structural/` | Testing external dependency failures and input edge cases |
| `04_concurrency/` | Testing concurrent access correctness |
| `05_load/` | Measuring behavior under sustained load |
| `06_security/` | Testing auth rules and ownership |
| `07_reliability/` | What we'd test if we had the infrastructure (plan only) |
| `compound_prompt/` | The combined prompt — built piece by piece, not magic |

Each folder contains a `prompt.md` (the AI prompt that generated the tests), a `plan.md` (what it decided to test and why), and the test file itself. Round 1 has no prompt — the point is you can write that round yourself.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Start the servers

Open two terminal windows:

**Terminal 1 — Moderation service (port 5001):**
```bash
python moderation_service/app.py
```

**Terminal 2 — Main server (port 5000):**
```bash
python server/app.py
```

Both servers use in-memory storage. Restart them to reset all data.

---

## Run the tests

```bash
pytest 00_green_mirage/ 01_api_level/ 02_feature_level/ 03_structural/ 04_concurrency/ 06_security/ -v
```

Round 05 is a Locust load test (see below). Round 07 has no executable tests.

---

## Run the load test

Both servers must be running first.

```bash
locust -f 05_load/locustfile.py --headless -u 100 -r 10 -t 30s --host http://localhost:5000
```

---

## The progression

**Green Mirage** — Two status code assertions. Looks like a test. Proves almost nothing.

**Round 1: API Level** — Test the response body. Do the fields exist? Are the values right? Does the server reject bad input? You don't need AI for this.

**Round 2: Feature Level** — Test the feature, not the endpoint. Does the review appear when you list? Does an edit show up everywhere? Does a delete actually delete?

**Round 3: Structural** — You now know the server calls a moderation service. What happens when it rejects, fails, or times out? What about malformed input?

**Round 4: Concurrency** — 10 simultaneous submissions. No lost data, no duplicates. The lock either works or it doesn't.

**Round 5: Load** — Sustained traffic. Where does it start to bend?

**Round 6: Security** — Who can do what? Can user B delete user A's review? What happens with no token?

**Round 7: Reliability** — The tests you can't write yet. Naming the gap is the first step to closing it.

**Compound Prompt** — Everything from rounds 2–7 combined into one prompt. The audience saw it built piece by piece. It's not magic.
