import time

POLL_INTERVAL_S = 10


def run(fetch_jobs, handle):
    while True:
        for job in fetch_jobs():
            handle(job)
        time.sleep(POLL_INTERVAL_S)
