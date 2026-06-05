#!/usr/bin/env python3
"""Extract final assistant response + workspace.dsl from subagent JSONL transcripts."""
import json
import os
import re
import sys

TASKS_DIR = "/tmp/claude-1000/-home-cassiobotaro-Projetos-skills/3654c1dc-e0f0-477e-9978-d4f0e688cd73/tasks"
ITER_DIR = os.path.dirname(os.path.abspath(__file__))

RUNS = {
    "a20829050810fa872": ("eval-1-ambiguous-spec/with_skill", 34068, 110261, 11),
    "a68b715532326bdde": ("eval-1-ambiguous-spec/without_skill", 11370, 63607, 4),
    "a7b4f5c191bdd6a02": ("eval-2-complete-workspace/with_skill", 33942, 114813, 10),
    "a2945cb22442db9fe": ("eval-2-complete-workspace/without_skill", 13388, 81805, 7),
    "a236cb78d6aad9216": ("eval-3-evolve-existing/with_skill", 34141, 107010, 13),
    "a74df70f5d53e0417": ("eval-3-evolve-existing/without_skill", 16946, 92252, 9),
    "ae79734a90c0f7ae2": ("eval-4-landscape/with_skill", 36128, 87965, 12),
    "a5270283e088f7daa": ("eval-4-landscape/without_skill", 12097, 69163, 4),
}

NOTE = ("Write/Bash permissions auto-denied for background agent; DSL delivered in "
        "final response text and extracted to outputs/ by the orchestrator.")


def last_assistant_text(path):
    texts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message", obj)
            if obj.get("type") != "assistant" and msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, list):
                chunk = "\n".join(c.get("text", "") for c in content
                                  if isinstance(c, dict) and c.get("type") == "text").strip()
                if chunk:
                    texts.append(chunk)
            elif isinstance(content, str) and content.strip():
                texts.append(content.strip())
    return texts[-1] if texts else None


def extract_dsl(text):
    fences = re.findall(r"```(?:dsl)?\s*\n(.*?)```", text, flags=re.DOTALL)
    candidates = [f for f in fences if f.lstrip().startswith("workspace")]
    return candidates[-1] if candidates else None


def main():
    for task_id, (rel, tokens, ms, tools) in RUNS.items():
        run_dir = os.path.join(ITER_DIR, rel)
        out_dir = os.path.join(run_dir, "outputs")
        os.makedirs(out_dir, exist_ok=True)
        src = os.path.join(TASKS_DIR, task_id + ".output")
        text = last_assistant_text(src)
        if not text:
            print(f"WARN {rel}: no assistant text found", file=sys.stderr)
            continue
        with open(os.path.join(out_dir, "final_response.md"), "w") as f:
            f.write(text)
        dsl = extract_dsl(text)
        if dsl:
            with open(os.path.join(out_dir, "workspace.dsl"), "w") as f:
                f.write(dsl if dsl.endswith("\n") else dsl + "\n")
            dsl_status = f"dsl={len(dsl.splitlines())} lines"
        else:
            dsl_status = "NO DSL FENCE FOUND"
        with open(os.path.join(run_dir, "timing.json"), "w") as f:
            json.dump({"total_tokens": tokens, "duration_ms": ms,
                       "total_duration_seconds": round(ms / 1000, 1),
                       "tool_uses": tools, "note": NOTE}, f, indent=2)
        print(f"OK {rel}: response={len(text)} chars, {dsl_status}")


if __name__ == "__main__":
    main()
