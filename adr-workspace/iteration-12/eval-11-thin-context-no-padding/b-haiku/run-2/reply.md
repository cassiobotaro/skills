I wrote ADR 0003, "Store user-uploaded files in S3", as Accepted, in doc/adr/0003-store-user-uploaded-files-in-s3.md. It records the decision, the autoscaling reason, and the accepted network-call cost. I did not add a supersede or amend link, because nothing in the log covers file storage yet.

A few things I could not tell from your message and did not put in the ADR:

1. Were other options considered, such as a shared network volume (EFS) or keeping the files on the servers with a different replacement policy? If so, a short list would make the record more useful to future readers.
2. What happens to the files already on the servers? Is there a migration to S3, and is it part of this decision or a separate one?
3. Are there constraints the ADR should name, such as the S3 bucket's region, encryption, or access control?
