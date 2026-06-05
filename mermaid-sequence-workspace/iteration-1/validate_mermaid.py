#!/usr/bin/env python3
"""Extract every ```mermaid block from each run's answer.md and validate it
against the official Mermaid MCP server (mcp.mermaid.ai) over plain HTTP.
mermaid-cli is unusable on this machine (puppeteer Chrome not installed).
Writes validation.json per run dir and prints a summary table."""

import json
import re
import sys
import urllib.request
from pathlib import Path

ITER = Path(__file__).parent
BLOCK_RE = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
URL = "https://mcp.mermaid.ai/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def rpc(payload: dict, session: str | None = None) -> tuple[dict | None, str | None]:
    headers = dict(HEADERS)
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=90) as resp:
        sid = resp.headers.get("Mcp-Session-Id", session)
        body = resp.read().decode()
    for line in body.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:]), sid
    return None, sid


def new_session() -> str:
    _, sid = rpc({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                   "clientInfo": {"name": "skill-eval-grader", "version": "0.0.1"}},
    })
    rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def validate_block(sid: str, code: str, name: str, rpc_id: int) -> dict:
    data, _ = rpc({
        "jsonrpc": "2.0", "id": rpc_id, "method": "tools/call",
        "params": {"name": "validate_and_render_mermaid_diagram", "arguments": {
            "prompt": f"eval grading {name}", "mermaidCode": code,
            "diagramType": "sequenceDiagram", "clientName": "claude",
        }},
    }, sid)
    valid, error, link = False, "", ""
    for c in data.get("result", {}).get("content", []):
        if c.get("type") != "text":
            continue
        t = c["text"]
        if "INVALID" in t:
            m = re.search(r"\*\*Error:\*\* (.*?)(?:\n\n|\Z)", t, re.DOTALL)
            error = (m.group(1).strip() if m else t[:300])[:400]
        if "Diagram Generated" in t:
            valid = True
        m = re.search(r"Preview/Edit Link:\*\* (\S+)", t)
        if m:
            link = m.group(1)
    return {
        "block": name,
        "lines": len(code.strip().splitlines()),
        "messages": sum(1 for l in code.splitlines()
                        if re.search(r"(->>|-->>|--\)|-\)|--x|-x)", l)),
        "valid": valid,
        "error": error,
        "preview_link": link,
    }


def main():
    sid = new_session()
    rpc_id = 10
    for answer in sorted(ITER.glob("eval-*/*/outputs/answer.md")):
        run_dir = answer.parent.parent
        key = f"{run_dir.parent.name}/{run_dir.name}"
        blocks = BLOCK_RE.findall(answer.read_text())
        run = []
        for i, code in enumerate(blocks):
            rpc_id += 1
            run.append(validate_block(sid, code, f"{key}#{i}", rpc_id))
        summary = {
            "validator": "mcp.mermaid.ai validate_and_render_mermaid_diagram",
            "blocks": len(run),
            "all_valid": all(b["valid"] for b in run) if run else None,
            "results": run,
        }
        (run_dir / "validation.json").write_text(json.dumps(summary, indent=2) + "\n")
        if not run:
            print(f"{key}: no mermaid blocks")
            continue
        status = "ALL VALID" if summary["all_valid"] else "INVALID"
        sizes = ", ".join(f"#{i}:{b['messages']}msg/{'ok' if b['valid'] else 'FAIL'}"
                          for i, b in enumerate(run))
        print(f"{key}: {len(run)} block(s) [{status}] {sizes}")
        for b in run:
            if not b["valid"]:
                print(f"    {b['block']}: {b['error'][:250]}")


if __name__ == "__main__":
    sys.exit(main())
