I wrote ADR 0003, "Store user-uploaded files in S3", in doc/adr/ as Accepted, recording the move from application-server local disk to S3 and the accepted trade-off that every file read becomes a network call.

Questions for you:

1. Were any other options considered for storing the files, such as a shared network volume or an object store other than S3? If so, name them and the reason each was rejected. I left the Alternatives out of the ADR because you did not mention any.
2. Is the existing library of files on the app servers going to be migrated to S3? If so, is that part of this decision or a separate one? The ADR does not say how existing files move.
3. Is the decision already agreed, or should it be recorded as Proposed until the team signs off? I recorded it as Accepted because you described it as a move already underway.

Reply with answers and I will amend the ADR, or supersede it if the decision changes.
