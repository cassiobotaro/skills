import os

import boto3

LINK_TTL_SECONDS = 24 * 60 * 60


def notify(account_id: str, key: str) -> None:
    url = boto3.client("s3").generate_presigned_url(
        "get_object",
        Params={"Bucket": os.environ["EXPORT_BUCKET"], "Key": key},
        ExpiresIn=LINK_TTL_SECONDS,
    )
    boto3.client("ses").send_email(
        Source=os.environ["MAIL_FROM"],
        Destination={"ToAddresses": [f"{account_id}@accounts.example.com"]},
        Message={
            "Subject": {"Data": "Your export is ready"},
            "Body": {"Text": {"Data": url}},
        },
    )
