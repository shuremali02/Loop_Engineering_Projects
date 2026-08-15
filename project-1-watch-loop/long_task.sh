#!/usr/bin/env bash
# Simulates a long-running task (e.g. a build or migration).
# Sleeps, then writes a marker file so a watcher can detect completion.
set -euo pipefail

DURATION="${1:-60}"  # seconds, default 1 minute

echo "Task started at $(date -Iseconds)" > task.log
sleep "$DURATION"
echo "Task finished at $(date -Iseconds)" >> task.log
echo "done" > task_done.txt
