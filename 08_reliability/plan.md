# Round 8: Reliability (Plan Only)

The scenarios below require infrastructure we don't have: persistent storage, multiple nodes, a backup/restore system, a time-zone-aware test harness.

## Test Plan

**1. Data persistence after restart**
- Write 50 reviews. Stop the server. Start it again. All 50 reviews should still exist.
- Current implementation: in-memory store. This fails immediately on restart.

**2. Geographic consistency**
- Create a review through node A. Read it from node B (different region).
- Requires load balancer and at least two instances.

**3. Failover consistency**
- Reviews on the primary should survive failover to a replica.
- Requires replication and a failover mechanism to trigger.

**4. Backup and restore**
- Take a snapshot. Add 100 reviews. Restore the snapshot. Verify only the pre-snapshot reviews exist.
- Tests that restore doesn't silently merge or discard data.

**5. Timestamp accuracy across time zones**
- Submit reviews from clients reporting different local times.
- All timestamps should be stored in UTC and remain consistent regardless of client locale.

**6. Deterministic ordering after restart**
- Reviews listed via GET /books/{bookId}/reviews should appear in the same order after a restart.
- Current implementation: list insertion order. After a restart with a real DB, ordering depends on the query.

