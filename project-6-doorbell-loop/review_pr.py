#!/usr/bin/env python3
"""Automated PR reviewer for the doorbell loop.

Fired by GitHub Actions on pull_request: [opened, synchronize]. Scans
changed .py files with Python's own ast module for one real bug class:
a parameter that defaults to None but is used in an arithmetic
operation without an `is None` guard anywhere in the function. Posts
the finding (or a clean bill) as a real PR comment via `gh pr comment`.
"""
import ast
import os
import subprocess
import sys


def changed_py_files(base_sha, head_sha):
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}...{head_sha}"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [f for f in out.splitlines() if f.endswith(".py")]


def is_guarded(func_node, param_name):
    for node in ast.walk(func_node):
        if isinstance(node, ast.Compare) and isinstance(node.left, ast.Name) \
                and node.left.id == param_name:
            for op, comparator in zip(node.ops, node.comparators):
                if isinstance(op, (ast.Is, ast.IsNot)) and \
                        isinstance(comparator, ast.Constant) and comparator.value is None:
                    return True
    return False


def used_unsafely(func_node, param_name):
    for node in ast.walk(func_node):
        if isinstance(node, ast.BinOp):
            for side in (node.left, node.right):
                if isinstance(side, ast.Name) and side.id == param_name:
                    return True
    return False


def check_file(path):
    findings = []
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        args = node.args.args
        defaults = node.args.defaults
        offset = len(args) - len(defaults)
        for i, default in enumerate(defaults):
            if isinstance(default, ast.Constant) and default.value is None:
                param_name = args[offset + i].arg
                if not is_guarded(node, param_name) and used_unsafely(node, param_name):
                    findings.append((path, node.lineno, node.name, param_name))
    return findings


def main():
    base_sha = os.environ["BASE_SHA"]
    head_sha = os.environ["HEAD_SHA"]
    pr_number = os.environ["PR_NUMBER"]

    findings = []
    for path in changed_py_files(base_sha, head_sha):
        if os.path.exists(path):
            findings.extend(check_file(path))

    if findings:
        lines = ["**Review summary**", "", "Correctness bug(s) found:", ""]
        for path, lineno, func, param in findings:
            lines.append(
                f"- **`{path}:{lineno}`** — `{func}()` has `{param}=None` "
                f"but uses `{param}` directly in an arithmetic operation, "
                f"with no `{param} is None` guard anywhere in the function. "
                f"Calling `{func}(...)` without `{param}` (the "
                f"default-argument case the signature explicitly allows) "
                f"raises `TypeError: unsupported operand type(s)`."
            )
        lines.append("")
        lines.append(
            "_Automated review — project-6-doorbell-loop's AST-based "
            "checker (Loop Engineering, Concept 7/10)._"
        )
    else:
        lines = [
            "No correctness issues found by the automated checker.",
            "",
            "_Automated review — project-6-doorbell-loop's AST-based checker._",
        ]

    body = "\n".join(lines)
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", body], check=True)
    print(body)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
