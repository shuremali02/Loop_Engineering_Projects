#!/usr/bin/env python3
"""Reviewer agent: grades a fix attempt PASS or FAIL.

Runs the real test suite in the given worktree. PASS only if every test
passes. On FAIL, prints the actual failure reasons from the test runner
(not an opinion) so the maker knows exactly what is still wrong.
"""
import subprocess
import sys


def review(worktree_path):
    result = subprocess.run(
        ["python3", "-m", "unittest", "test_inventory", "-v"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )
    passed = result.returncode == 0
    verdict = "PASS" if passed else "FAIL"
    print(f"[reviewer] Verdict: {verdict}")
    print(result.stderr)
    return passed, result.stderr


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    ok, _ = review(path)
    sys.exit(0 if ok else 1)
