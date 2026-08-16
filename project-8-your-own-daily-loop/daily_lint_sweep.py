#!/usr/bin/env python3
"""Project 8's daily loop body: maker-checker lint sweep of this repo's
.py files, run inside an isolated git worktree, PR'd only on a real PASS.

Heartbeat: fired by a CronCreate job, once daily, for 7 days.
Worktree:  fresh git worktree per firing, deleted after.
Skill:     .claude/skills/daily-lint-sweep/SKILL.md documents this.
Maker:     scoped auto-fix for exactly one safe, mechanical issue class
           (F541 "f-string is missing placeholders" -> strip the f-prefix).
           Everything else pyflakes finds is reported, never auto-fixed.
Checker:   re-runs pyflakes on the fixed worktree; PASS only if every
           line we touched is confirmed clean in fresh output.
Connector: opens a real PR via `gh pr create`, only on a real PASS with a
           real diff.
Spine:     appends a dated entry to progress.md (outside the worktree, so
           it survives worktree cleanup) every single firing, pass or not.
Budget guard: MAX_AUTO_FIX caps how many lines one firing will touch; over
           that, the run skips auto-fixing entirely and logs NEEDS HUMAN
           instead of taking a wide, unreviewed action.
"""
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS = PROJECT_DIR / "progress.md"
MAX_AUTO_FIX = 5
FSTRING_MSG = "f-string is missing placeholders"


def run(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def repo_root():
    return Path(run(["git", "rev-parse", "--show-toplevel"]).stdout.strip())


def pyflakes(paths):
    """Real checker step: pyflakes exit code decides pass/fail, not us."""
    result = subprocess.run(
        ["/usr/bin/python3", "-m", "pyflakes", *[str(p) for p in paths]],
        capture_output=True, text=True,
    )
    findings = []
    for line in result.stdout.splitlines():
        m = re.match(r"^(.+):(\d+):(\d+): (.+)$", line)
        if m:
            findings.append({
                "path": m.group(1), "line": int(m.group(2)),
                "col": int(m.group(3)), "msg": m.group(4),
            })
    return findings


def py_files(root):
    """root is a worktree checkout — .worktrees/ is gitignored so it's
    never checked out inside one; only .git needs excluding here."""
    return sorted(p for p in root.rglob("*.py") if ".git" not in p.parts)


def fix_fstring_line(path, lineno):
    lines = path.read_text().splitlines(keepends=True)
    idx = lineno - 1
    original = lines[idx]
    fixed = re.sub(r'\bf(["\'])', r"\1", original, count=1)
    if fixed == original:
        return False
    lines[idx] = fixed
    path.write_text("".join(lines))
    return True


def spine_entry(text):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(PROGRESS, "a") as f:
        f.write(f"\n### {today}\n{text}\n")
    print(f"[daily-lint-sweep] {text}")


def main():
    root = repo_root()
    tag = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch = f"lint-sweep/{tag}"
    worktree = root / ".worktrees" / f"lint-sweep-{tag}"

    tries = 0
    while True:
        result = run(["git", "worktree", "add", "-q", str(worktree), "-b", branch],
                      cwd=root, check=False)
        if result.returncode == 0:
            break
        tries += 1
        if tries >= 5:
            spine_entry(f"NEEDS HUMAN: could not create worktree after {tries} tries "
                        f"({result.stderr.strip()[:200]})")
            return 1
        import time
        time.sleep(0.5)

    try:
        files = py_files(worktree)
        findings = pyflakes(files)

        if not findings:
            spine_entry("Clean sweep — 0 issues found across "
                        f"{len(files)} .py file(s). No PR needed.")
            return 0

        fixable = [f for f in findings if f["msg"] == FSTRING_MSG]
        out_of_scope = [f for f in findings if f["msg"] != FSTRING_MSG]

        if len(fixable) > MAX_AUTO_FIX:
            spine_entry(
                f"NEEDS HUMAN: found {len(fixable)} auto-fixable issues, "
                f"over the budget guard of {MAX_AUTO_FIX} per run — skipping "
                f"auto-fix entirely rather than taking a wide unreviewed "
                f"action. {len(out_of_scope)} other issue(s) also found, "
                f"out of this loop's scope (not auto-fixed)."
            )
            return 1

        if not fixable:
            summary = "; ".join(
                f"{f['path'].replace(str(worktree) + '/', '')}:{f['line']} {f['msg']}"
                for f in out_of_scope
            )
            spine_entry(
                f"Found {len(out_of_scope)} issue(s), 0 auto-fixed "
                f"(all out of this loop's scope — needs human review): {summary}"
            )
            return 0

        fixed = []
        for f in fixable:
            if fix_fstring_line(Path(f["path"]), f["line"]):
                fixed.append(f)

        # Checker: real re-run, not self-judgment. PASS only if every line
        # we touched is confirmed clean in fresh pyflakes output.
        after = pyflakes(py_files(worktree))
        still_broken = [
            a for a in after
            if a["msg"] == FSTRING_MSG
            and any(a["path"] == f["path"] and a["line"] == f["line"] for f in fixed)
        ]

        if still_broken:
            spine_entry(
                f"FAIL: attempted {len(fixed)} auto-fix(es), "
                f"{len(still_broken)} still failing after fix — reviewer "
                f"rejected, no PR opened."
            )
            return 1

        diff = run(["git", "status", "--porcelain"], cwd=worktree).stdout.strip()
        if not diff:
            spine_entry("PASS but no real diff produced — nothing to PR.")
            return 0

        run(["git", "add", "-A"], cwd=worktree)
        run(["git", "commit", "-m",
             f"daily-lint-sweep: fix {len(fixed)} f-string-without-placeholder issue(s)"],
            cwd=worktree)
        run(["git", "push", "-u", "origin", branch], cwd=worktree)

        rel_files = sorted({f["path"].replace(str(worktree) + "/", "") for f in fixed})
        pr_body = (
            f"Automated daily lint sweep (Project 8). Fixed {len(fixed)} "
            f"real pyflakes finding(s) — f-string(s) with no placeholder — "
            f"in: {', '.join(rel_files)}.\n\n"
            f"Reviewer re-ran pyflakes after the fix and confirmed every "
            f"touched line is clean before this PR was opened."
        )
        pr = run(["gh", "pr", "create", "--title",
                  f"daily-lint-sweep: {len(fixed)} fix(es) ({tag})",
                  "--body", pr_body, "--base", "main", "--head", branch],
                 cwd=worktree)
        pr_url = pr.stdout.strip()

        scope_note = (
            f" ({len(out_of_scope)} other issue(s) found, out of scope, not "
            f"auto-fixed)" if out_of_scope else ""
        )
        spine_entry(
            f"PASS — fixed {len(fixed)} issue(s), reviewer confirmed clean, "
            f"PR opened: {pr_url}{scope_note}"
        )
        return 0
    finally:
        run(["git", "worktree", "remove", "--force", str(worktree)], cwd=root, check=False)


if __name__ == "__main__":
    sys.exit(main())
