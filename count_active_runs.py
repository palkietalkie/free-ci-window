from __future__ import annotations

from check_private_ci_is_blocked import ORG
from run_gh import run_gh


def count_active_runs(repo: str) -> int:
    return int(
        run_gh(
            "run", "list", "--repo", f"{ORG}/{repo}", "--json", "status",
            "-q", '[.[] | select(.status=="in_progress" or .status=="queued")] | length',
        )
    )
