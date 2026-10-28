from __future__ import annotations

from check_private_ci_is_blocked import ORG
from check_private_ci_is_blocked import main as check_private_ci_is_blocked
from find_due_workflows import Schedule
from read_visibility import read_visibility
from set_visibility import set_visibility


def open_window(due: list[Schedule]) -> list[str]:
    """The repos flipped public for this hour, which are the ones to flip back; none when private Actions run normally."""
    # check_private_ci_is_blocked exits 0 when blocked.
    if check_private_ci_is_blocked() != 0:
        print("private Actions run normally; nothing to open")
        return []

    opened = []
    for repo in sorted({schedule.repo for schedule in due}):
        if read_visibility(repo) == "PRIVATE":
            print(f"private Actions are refused; flipping {ORG}/{repo} public for this hour's runs")
            set_visibility(repo, "public")
            opened.append(repo)
    return opened
