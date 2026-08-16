#!/usr/bin/env python3
"""Project 3's morning-brief loop, taken as-is for Project 7's rehearsal.
Scans sample_repo for open TODOs, diffs against progress.md's memory,
and appends a dated entry to run_log.md. This is the PRE-FIX version:
it does not check that sample_repo exists before scanning it."""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
REPO = ROOT / "sample_repo"
PROGRESS = ROOT / "progress.md"
RUN_LOG = ROOT / "run_log_entries.txt"

TODO_RE = re.compile(r"TODO.*")


def scan_todos():
    if not REPO.exists() or not REPO.is_dir():
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"NEEDS HUMAN: sample_repo not found at {REPO} — nothing was scanned"
        with open(RUN_LOG, "a") as f:
            f.write(f"[{today}] {msg}\n")
        print(f"[loop-runner] {msg}", file=sys.stderr)
        sys.exit(1)
    found = []
    for path in sorted(REPO.rglob("*.py")):
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            m = TODO_RE.search(line)
            if m:
                found.append(f"{path.name}:{lineno}: {m.group(0).strip()}")
    return found


def read_recorded():
    if not PROGRESS.exists():
        return set(), ""
    text = PROGRESS.read_text()
    recorded = set()
    in_section = False
    for line in text.splitlines():
        if line.startswith("## Recorded TODOs"):
            in_section = True
            continue
        if in_section:
            if line.startswith("## "):
                break
            if line.startswith("- "):
                recorded.add(line[2:].strip())
    return recorded, text


def main():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    current = scan_todos()
    recorded, existing_text = read_recorded()
    new_items = [item for item in current if item not in recorded]

    if not PROGRESS.exists():
        header = (
            "# Break-It-On-Purpose — Progress Spine\n\n"
            "## Recorded TODOs (cumulative — do not repeat these)\n"
        )
        body = "".join(f"- {item}\n" for item in current)
        existing_text = header + body + "\n## Run history\n"

    all_recorded = recorded | set(current)
    lines = existing_text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## Recorded TODOs"):
            out.append(line)
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            for item in sorted(all_recorded):
                out.append(f"- {item}")
            out.append("")
            continue
        out.append(line)
        i += 1

    if new_items:
        entry = [f"\n### {today}", f"Found {len(new_items)} new TODO(s):"]
        entry += [f"- {item}" for item in new_items]
    else:
        entry = [f"\n### {today}", "No new TODOs found — same as last run."]

    out.extend(entry)
    PROGRESS.write_text("\n".join(out) + "\n")

    log_line = f"[{today}] scanned={len(current)} new={len(new_items)}\n"
    with open(RUN_LOG, "a") as f:
        f.write(log_line)

    print(f"[loop-runner] Scanned {len(current)} TODO(s) total.")
    print(f"[loop-runner] {len(new_items)} new since last run.")
    print(log_line.strip())


if __name__ == "__main__":
    sys.exit(main())
