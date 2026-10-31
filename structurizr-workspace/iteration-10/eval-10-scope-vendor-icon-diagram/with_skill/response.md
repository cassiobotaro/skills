This isn't a job for the Structurizr / C4 skill, so I haven't started a `workspace.dsl`.

What you're describing — EC2, RDS, S3 and CloudFront boxes drawn with the official AWS icons, in the style of an AWS reference architecture — is a cloud-infrastructure picture in the vendor's own iconography. C4 models the software abstractions your team owns (people, systems, containers and how they talk to each other), not a vendor service catalog, so forcing it into a C4 workspace would give you a worse picture than a diagramming tool will.

Tools that produce exactly that picture:

- **diagrams.net / draw.io** — ships the official AWS architecture shape library (Shapes panel → "+ More Shapes" → AWS); free, exports PNG/SVG.
- **Diagrams** (the Python `diagrams` package) — diagrams-as-code with the AWS icon set; your five nodes are about a dozen lines and the script can live in the repo next to the infrastructure code.
- **AWS Architecture Icons** (the official asset pack at aws.amazon.com/architecture/icons) for PowerPoint, Figma or Lucidchart.

If you'd like, I can write the `diagrams` Python script for the topology you listed — CloudFront in front, two EC2 app servers, the RDS Postgres instance and the S3 uploads bucket — just say so.

Where this skill *would* fit: if, beyond the picture, you also want the platform documented as a C4 model (what software runs on those EC2 instances, who uses it, what it integrates with), I can produce a `workspace.dsl` with a system context view, a container view and an AWS deployment view — Structurizr's AWS theme puts the service icons on the deployment nodes there. For that I'd need three things: (1) what runs on the two EC2 instances — one application or several services? (2) who the users of the platform are, and (3) which external systems it talks to. Answer those and I'll start.
