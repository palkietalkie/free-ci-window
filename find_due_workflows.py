#!/usr/bin/env python3
"""Print the `<repo> <workflow file>` pairs due in the given UTC hour, one per line, for the hourly workflow to dispatch.

The schedules live here rather than as `schedule:` triggers in each private repo because a private repo's own cron cannot be trusted to run: when GitHub refuses private Actions, a cron fires into a refusal, and a public window opened at a fixed minute only helps the runs GitHub happens to start inside it (scheduled runs start late, worst at the top of the hour). Dispatching from here, after the window is open, starts each run at the moment it can run."""

from __future__ import annotations

import sys
from dataclasses import dataclass

EVERY_HOUR = tuple(range(24))


@dataclass(frozen=True)
class Schedule:
    repo: str
    "The repo under the palkietalkie org that holds the workflow."
    workflow: str
    "The workflow's file name, as `gh workflow run` takes it."
    utc_hours: tuple[int, ...]
    "The UTC hours it runs in; each job reads the time itself, so the minute within the hour does not matter."


# 03:00 UTC is the quiet hour for every timezone the app serves, so a user opening Topics never catches the daily swap mid-write. 16:00 UTC is 09:00 Pacific while PDT and 08:00 while PST, when the morning reports are read.
SCHEDULES = (
    Schedule(repo="backend", workflow="send-scheduled-push-notifications.yml", utc_hours=EVERY_HOUR),
    Schedule(repo="backend", workflow="refresh-daily-content.yml", utc_hours=(3,)),
    Schedule(repo="backend", workflow="neo4j-keepalive.yml", utc_hours=(6,)),
    Schedule(repo="backend", workflow="daily-cost-report.yml", utc_hours=(16,)),
    Schedule(repo="backend", workflow="daily-gtm-funnel.yml", utc_hours=(16,)),
)


def find_due_workflows(*, schedules: tuple[Schedule, ...], utc_hour: int) -> list[Schedule]:
    return [schedule for schedule in schedules if utc_hour in schedule.utc_hours]


def main() -> int:
    for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=int(sys.argv[1])):
        print(schedule.repo, schedule.workflow)
    return 0


if __name__ == "__main__":
    sys.exit(main())
