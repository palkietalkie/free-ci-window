#!/usr/bin/env python3
"""Run the workflows due this UTC hour: open the free-CI window on any private repo GitHub would refuse, dispatch each due workflow, and close the window once their runs finish.

Kept here rather than inline in the workflow file so it can be read, linted and tested like the rest of the repo; the workflow only calls it."""

from __future__ import annotations

import os
import sys
import time
from datetime import UTC, datetime

from check_private_ci_is_blocked import ORG
from close_window import close_window
from find_due_workflows import SCHEDULES, find_due_workflows
from open_window import open_window
from run_gh import run_gh

# A dispatched run takes a few seconds to be listed, so it is waited for before counting what is still active.
SECONDS_FOR_A_DISPATCH_TO_APPEAR = 20


def main() -> int:
    due = find_due_workflows(schedules=SCHEDULES, utc_hour=datetime.now(UTC).hour)
    if not due:
        print("nothing due this hour")
        return 0

    opened = open_window(due)
    for schedule in due:
        print(f"dispatching {schedule.repo} {schedule.workflow}")
        # The admin token administers visibility and nothing else, so starting a workflow takes the dispatch token.
        run_gh("workflow", "run", schedule.workflow, "--repo", f"{ORG}/{schedule.repo}", token=os.environ["GH_DISPATCH_TOKEN"])
    if opened:
        time.sleep(SECONDS_FOR_A_DISPATCH_TO_APPEAR)
    close_window(opened)
    return 0


if __name__ == "__main__":
    sys.exit(main())
