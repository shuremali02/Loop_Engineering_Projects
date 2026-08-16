#!/usr/bin/env bash
# Codified fix-loop body (Project 4) as ONE command.
# Fans out N candidate fixes into isolated worktrees in parallel (&/wait),
# grades each with the real reviewer, and prints a verdict table.
# Has NO memory: every run starts from the same buggy base and re-does
# everything from scratch. Run twice to see this for yourself.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJ="$ROOT/project-5-codify-body"
RESULTS_DIR=$(mktemp -d)

# candidate_name : sed expression that applies the fix
declare -A CANDIDATES=(
  [average]='s/return sum(numbers) \/\/ len(numbers)/return sum(numbers) \/ len(numbers)/'
  [truncate]='s/text\[:length - 1\]/text[:length]/'
  [is_weekend]='s/day_index in (6, 7)/day_index in (5, 6)/'
)

# candidate_name : the specific test(s) that prove *that* candidate's fix
declare -A CANDIDATE_TESTS=(
  [average]="test_utils.TestUtils.test_average"
  [truncate]="test_utils.TestUtils.test_truncate"
  [is_weekend]="test_utils.TestUtils.test_is_weekend_saturday test_utils.TestUtils.test_is_weekend_sunday"
)

run_candidate() {
  local name="$1" sed_expr="$2" tests="$3"
  local tag="${name}-$$-$RANDOM"
  local wt="$ROOT/.worktrees/codify-$tag"
  # git worktree add races on shared .git metadata when run truly
  # concurrently; retry a few times on lock contention.
  local tries=0
  until git -C "$ROOT" worktree add -q "$wt" -b "codify/$tag" \
      > "$RESULTS_DIR/$name.setup.log" 2>&1; do
    tries=$((tries + 1))
    if [ "$tries" -ge 5 ]; then
      echo "FAIL (worktree setup failed, see $name.setup.log)" > "$RESULTS_DIR/$name.verdict"
      return
    fi
    sleep 0.3
  done
  sed -i "$sed_expr" "$wt/project-5-codify-body/sample_repo/utils.py"
  if python3 "$PROJ/reviewer.py" "$wt/project-5-codify-body/sample_repo" $tests \
      > "$RESULTS_DIR/$name.log" 2>&1; then
    echo "PASS" > "$RESULTS_DIR/$name.verdict"
  else
    echo "FAIL" > "$RESULTS_DIR/$name.verdict"
  fi
  git -C "$ROOT" worktree remove --force "$wt" >/dev/null 2>&1
  git -C "$ROOT" branch -D "codify/$tag" >/dev/null 2>&1
}

echo "[codify-body] Fanning out ${#CANDIDATES[@]} candidates in parallel..."
for name in "${!CANDIDATES[@]}"; do
  run_candidate "$name" "${CANDIDATES[$name]}" "${CANDIDATE_TESTS[$name]}" &
done
wait

echo
echo "[codify-body] Verdicts:"
for name in "${!CANDIDATES[@]}"; do
  verdict=$(cat "$RESULTS_DIR/$name.verdict")
  echo "  - $name: $verdict"
done
rm -rf "$RESULTS_DIR"
