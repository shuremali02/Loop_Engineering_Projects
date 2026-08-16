#!/usr/bin/env python3
"""Same reviewer pattern as Project 4: real test command, real exit code."""
import subprocess
import sys


def review(worktree_path, test_targets):
    result = subprocess.run(
        ["python3", "-m", "unittest", *test_targets, "-v"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )
    passed = result.returncode == 0
    return passed, result.stderr


if __name__ == "__main__":
    targets = sys.argv[2:] if len(sys.argv) > 2 else ["test_utils"]
    ok, stderr = review(sys.argv[1], targets)
    print(f"[reviewer] Verdict: {'PASS' if ok else 'FAIL'}")
    print(stderr)
    sys.exit(0 if ok else 1)
