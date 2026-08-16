#!/usr/bin/env python3
"""Same reviewer pattern as Project 4: real test command, real exit code."""
import subprocess
import sys


def review(worktree_path):
    result = subprocess.run(
        ["python3", "-m", "unittest", "test_utils", "-v"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )
    passed = result.returncode == 0
    return passed, result.stderr


if __name__ == "__main__":
    ok, stderr = review(sys.argv[1])
    print(f"[reviewer] Verdict: {'PASS' if ok else 'FAIL'}")
    print(stderr)
    sys.exit(0 if ok else 1)
