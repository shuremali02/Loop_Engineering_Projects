# Run log — Project 4 (fix-loop)

Bug: `sample_repo/inventory.py`'s `days_of_stock_left` used true division
(`/`) instead of floor division (`//`), so `days_of_stock_left(10, 3)`
returned `3.3333333333333335` instead of `3`.

Base commit (buggy, on `main`): confirmed failing before any fix —
```
test_days_of_stock_left_full_days_only ... FAIL
AssertionError: 3.3333333333333335 != 3
Ran 4 tests in 0.007s
FAILED (failures=1)
```

## Attempt 1 (good fix) — worktree `.worktrees/fix-good`, branch `fix/days-of-stock-off-by-one`
Implementer changed `/` to `//`.

Reviewer (`python3 reviewer.py <worktree>/sample_repo`):
```
[reviewer] Verdict: PASS
test_apply_discount ... ok
test_days_of_stock_left_exact ... ok
test_days_of_stock_left_full_days_only ... ok
test_restock ... ok
Ran 4 tests in 0.001s
OK
```
Result: **PASS**. Fix committed on `fix/days-of-stock-off-by-one`.

## Attempt 2 (deliberately bad fix) — worktree `.worktrees/fix-bad`, branch `fix/days-of-stock-bad-attempt`
Implementer changed `current_stock / daily_usage` to
`current_stock // daily_usage + 1` (an off-by-one in the *other*
direction — a realistic wrong "fix").

Reviewer:
```
[reviewer] Verdict: FAIL
test_days_of_stock_left_exact ... FAIL
  AssertionError: 4 != 3
test_days_of_stock_left_full_days_only ... FAIL
  AssertionError: 4 != 3
Ran 4 tests in 0.006s
FAILED (failures=2)
```
Result: **FAIL, with concrete reasons** (which assertions failed and the
actual vs expected values). No PR was opened for this branch. The
worktree and branch were deleted after grading — it was only kept long
enough to prove the reviewer catches a bad fix, not to be merged.

## Conclusion
Both halves of the "Done when" criteria are demonstrated with real
command output: a good fix gets PASS (and proceeds to PR), and a
deliberately bad fix gets FAIL with reasons (and is not proposed as
a PR). The reviewer is not "soft" — it correctly rejected the bad
attempt using the same real test command as the checker, not agent
opinion.

## PR status
`fix/days-of-stock-off-by-one` is committed locally and ready to push.
Opening the actual GitHub PR is pending `gh auth login` completing in
this environment (git push here has no stored GitHub credentials — the
earlier root-repo push was done through a different credential path).
See README "How this was implemented" for the exact commands to finish
this once login completes.
