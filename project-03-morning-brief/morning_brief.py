#!/usr/bin/env python3
"""Scheduled loop: scan sample_repo for open TODOs, update progress.md
with only what is new since the last run. progress.md is the spine —
it is read at the start of every run and written at the end."""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
REPO = ROOT / "sample_repo"
PROGRESS = ROOT / "progress.md"

TODO_RE = re.compile(r"TODO.*")


def scan_todos():
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
            "# Morning Brief — Progress Spine\n\n"
            "This file is the loop's memory. Each run reads it, finds only "
            "*new* TODO comments since last time, and appends findings "
            "without repeating what is already recorded.\n\n"
            "## Recorded TODOs (cumulative — do not repeat these)\n"
        )
        body = "".join(f"- {item}\n" for item in current)
        history = "\n## Run history\n"
        existing_text = header + body + history

    all_recorded = recorded | set(current)

    # Rebuild the "Recorded TODOs" section from scratch each run.
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

    print(f"[morning-brief] Scanned {len(current)} TODO(s) total.")
    if new_items:
        print(f"[morning-brief] {len(new_items)} new since last run:")
        for item in new_items:
            print(f"  - {item}")
    else:
        print("[morning-brief] Nothing new — repo unchanged since last run.")
    print("[morning-brief] progress.md updated.")


if __name__ == "__main__":
    sys.exit(main())
