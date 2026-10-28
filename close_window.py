from __future__ import annotations

import time

from check_private_ci_is_blocked import ORG
from count_active_runs import count_active_runs
from read_visibility import read_visibility
from set_visibility import set_visibility

SECONDS_BETWEEN_CHECKS = 20


def close_window(opened: list[str]) -> None:
    for repo in opened:
        while count_active_runs(repo) > 0:
            time.sleep(SECONDS_BETWEEN_CHECKS)
        if read_visibility(repo) == "PUBLIC":
            print(f"runs finished; restoring {ORG}/{repo} to private")
            set_visibility(repo, "private")
