# Judge packet paa0e8b0a

You are grading one reply against a fixed list of yes/no checks. You did not write the
reply. Decide each check on its own, from the material below only.

Rules:
1. A check is MET only if you can quote the exact words (from the reply, or `file:line`
   from the files) that satisfy it. Put that quote in `evidence`.
2. A check is UNMET only after you looked: in `search`, say what you looked for and where
   (e.g. "any sentence naming a design doc, whole reply").
3. If it is borderline, it is UNMET. Say "borderline" in `search` and why.
4. Length, extra detail or extra files never make a check MET. Judge the proposition only.
5. Do not modify anything. Do not open any file other than this packet.

Return ONLY a JSON object, no prose around it:
{"packet": "paa0e8b0a", "checks": [{"id": "<check id>", "passed": true|false, "evidence": "<quote, or empty>", "search": "<what you looked for, or empty>"}]}
with exactly one entry per check listed below, in the same order.


## The user's message

ADR please: we're moving user-uploaded files from the app servers' local disk to S3, because the app servers are going into an autoscaling group next quarter and instances there get replaced without keeping their disks. Downside we accepted: every file read becomes a network call.

## The reply

I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md` (status Accepted, dated 2026-11-15). It follows the existing log, where 0002 is the latest record.

- **Context:** uploads live on the app servers' local disk. Next quarter the servers move into an autoscaling group, and instances there are replaced without keeping their disks.
- **Decision:** we will store user-uploaded files in S3.
- **Consequences:** files no longer depend on any single server's lifetime. The accepted downside is that every file read becomes a network call.

I added only what you told me. I didn't include alternatives, latency figures or migration steps, since you didn't give any. If you want those recorded, send them and I'll add them.

## Files in the project after the run

### doc/adr/0001-record-architecture-decisions.md (existed before the run)

```
  1| # 1. Record architecture decisions
  2| 
  3| Date: 2026-05-10
  4| 
  5| ## Status
  6| 
  7| Accepted
  8| 
  9| ## Context
 10| 
 11| We need to record the architectural decisions made on this project.
 12| 
 13| ## Decision
 14| 
 15| We will use Architecture Decision Records, as [described by Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).
 16| 
 17| ## Consequences
 18| 
 19| See Michael Nygard's article, linked above. For a lightweight ADR toolset, see Nat Pryce's [adr-tools](https://github.com/npryce/adr-tools).
```

### doc/adr/0002-use-postgresql-for-persistence.md (existed before the run)

```
  1| # 2. Use PostgreSQL for persistence
  2| 
  3| Date: 2026-05-12
  4| 
  5| ## Status
  6| 
  7| Accepted
  8| 
  9| ## Context
 10| 
 11| The service needs a relational store with strong transactional guarantees. The team has
 12| operational experience with PostgreSQL and the platform team already runs managed
 13| PostgreSQL clusters.
 14| 
 15| ## Decision
 16| 
 17| We will use PostgreSQL as the primary persistence layer for the service.
 18| 
 19| ## Consequences
 20| 
 21| Schema migrations become part of the deployment pipeline and must be reviewed.
 22| 
 23| We depend on the platform team's managed clusters for backups and failover.
```

### doc/adr/0003-store-user-uploaded-files-in-s3.md (NEW, written by the run)

```
  1| # 3. Store user-uploaded files in S3
  2| 
  3| Date: 2026-11-15
  4| 
  5| ## Status
  6| 
  7| Accepted
  8| 
  9| ## Context
 10| 
 11| User-uploaded files are currently stored on the local disk of the app servers. Next quarter the app servers will move into an autoscaling group, where instances are replaced without keeping their disks, so files kept on local disk would be lost whenever an instance is replaced.
 12| 
 13| ## Decision
 14| 
 15| We will store user-uploaded files in S3 instead of on the app servers' local disk.
 16| 
 17| ## Consequences
 18| 
 19| Uploaded files no longer depend on the lifetime of any single app server, so instances can be replaced freely in the autoscaling group.
 20| 
 21| Every file read becomes a network call, which is slower than reading from local disk. We accepted this trade-off.
```

## Checks

- **11.7** — The new ADR's Context section states the user's force: the app servers move to an autoscaling group next quarter, where replaced instances do not keep their disks
- **11.8** — The new ADR's Consequences section states the accepted trade-off: every file read becomes a network call
- **11.9** — The new ADR's Context section asserts nothing beyond the user's message and the two existing ADRs: no motive the user did not give, no general claim about S3, object storage, durability or common practice, no invented incident, number or alternative. Rewording the user's own statements is not an invention
- **11.10** — The new ADR's Decision and Consequences sections assert nothing beyond the user's message and the two existing ADRs. A consequence that is a direct logical restatement of the stated decision or trade-off is not an invention
