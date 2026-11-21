def summarize(rows):
    d = {}  # d maps account id to total bytes used
    for r in rows:
        # Negative bytes are billing corrections stored in the same table; not usage.
        if r["bytes"] < 0:
            continue
        d[r["account"]] = d.get(r["account"], 0) + r["bytes"]
    return d


def top_accounts(rows, n):
    totals = summarize(rows)
    return sorted(totals, key=totals.get, reverse=True)[:n]
