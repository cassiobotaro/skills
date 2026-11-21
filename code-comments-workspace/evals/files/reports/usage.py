def summarize(rows):
    d = {}  # d maps account id to total bytes used
    for r in rows:
        d[r["account"]] = d.get(r["account"], 0) + r["bytes"]
    return d


def top_accounts(rows, n):
    totals = summarize(rows)
    return sorted(totals, key=totals.get, reverse=True)[:n]
