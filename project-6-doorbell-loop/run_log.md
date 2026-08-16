# Project 6 — Run Log (real results)

## Mechanism

Claude Code Routines require a repo `environment_id` that can only be
provisioned by connecting the repo through the claude.ai Settings UI — a
manual step not reachable via any tool available in this session, and
confirmed by a real API error (`RemoteTrigger create` → HTTP 400:
`job_config must set ccr.environment_id`). Since the constraint for this
project is to stay on the `shuremali02` account/repo only, the event-driven
connector was implemented instead as a **native GitHub Actions workflow**
(`.github/workflows/pr-review.yml`), triggered on `pull_request: [opened,
synchronize]`. It runs a real AST-based static-analysis Python script
(`review_pr.py`, not an LLM) as the reviewer, using the `GITHUB_TOKEN`
Actions provides automatically, and posts a real PR comment via
`gh pr comment`. This is a genuine event-driven connector — deterministic
instead of LLM-based, which was surfaced to the user as an explicit
trade-off before building.

`review_pr.py`'s checker: for every function with a parameter defaulting to
`None`, flag it if the parameter is used directly in an arithmetic
operation (`ast.BinOp`) anywhere in the function body without an
`is None` / `is not None` guard anywhere in that body.

## Run 1 — PR #2 opened (`opened` event)

Branch `feature/shipping-calculator` added
`project-6-doorbell-loop/sample_repo/shipping.py` with two planted bugs:

```python
def calculate_shipping_cost(weight, discount=None):
    base_cost = weight * 5
    return base_cost - discount        # discount used with no None guard


def apply_bulk_rate(item_count, rate=None):
    return item_count * rate           # rate used with no None guard
```

PR opened: https://github.com/shuremali02/Loop_Engineering_Projects/pull/2

GitHub Actions run: `PR Doorbell Review` #31969734448 — fired automatically
on `opened`, completed in 13s, exit status `failure` (expected: the checker
exits 1 when it finds issues — that's the signal, not a crash).

Real PR comment posted, unprompted, flagging **both** planted bugs by exact
file/line/function/param, with the concrete `TypeError` failure mode:

> **Review summary**
>
> Correctness bug(s) found:
>
> - **`project-6-doorbell-loop/sample_repo/shipping.py:4`** — `calculate_shipping_cost()` has `discount=None` but uses `discount` directly in an arithmetic operation, with no `discount is None` guard anywhere in the function...
> - **`project-6-doorbell-loop/sample_repo/shipping.py:9`** — `apply_bulk_rate()` has `rate=None` but uses `rate` directly in an arithmetic operation, with no `rate is None` guard anywhere in the function...

## Run 2 — follow-up push to same PR (`synchronize` event)

Pushed a fix commit to the same branch, adding the missing guards:

```python
def calculate_shipping_cost(weight, discount=None):
    base_cost = weight * 5
    if discount is None:
        discount = 0
    return base_cost - discount


def apply_bulk_rate(item_count, rate=None):
    if rate is None:
        rate = 1
    return item_count * rate
```

GitHub Actions run: `PR Doorbell Review` #31969784600 — fired automatically
on `synchronize` (the push), completed in 9s, exit status `success`.

Second real PR comment posted, unprompted:

> No correctness issues found by the automated checker.

This is the **event heartbeat** proof: the loop re-fired on its own,
triggered purely by the push event, with no manual re-trigger.

## Outcome

PR #2 merged (`gh pr merge --merge --delete-branch`), merge commit
`103bbf4`. Both "Done when" conditions met:

1. The PR got a review nobody asked for, and it flagged both planted bugs
   with file/line/reason.
2. The follow-up push re-fired the review via `synchronize`, and the
   second review correctly reported clean.

With Projects 1–3, this completes all four heartbeats: in-session
(Project 1), conditional (Project 2), scheduled (Project 3), and
event-driven (Project 6).
