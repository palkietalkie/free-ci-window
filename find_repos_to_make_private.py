from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

# This repo is public on purpose: its own Actions are free, which is how it can act when the private repos cannot.
REPOS_PUBLIC_BY_DESIGN = frozenset({"free-ci-window"})

# A push flips its repo public a moment before it lands, and its runs take a moment more to queue, so a window this young is left for them.
MINUTES_FOR_A_PUSH_TO_START_ITS_RUNS = 15


@dataclass(frozen=True)
class RepoState:
    name: str
    "The repo under the palkietalkie org."
    visibility: str
    "PUBLIC or PRIVATE, as `gh repo list --json visibility` spells it."
    pushed_at: datetime
    "When the repo last received a push, which is about when the pre-push flip opened its window."
    active_runs: int
    "Its Actions runs queued or in progress."


def find_repos_to_make_private(*, repos: list[RepoState], now: datetime) -> list[str]:
    """The repos left public with nothing running, which enforce-private never closes when no run follows the flip (a repo with no workflows, or a push after its PR merged)."""
    oldest_young_push = now - timedelta(minutes=MINUTES_FOR_A_PUSH_TO_START_ITS_RUNS)
    return [
        repo.name
        for repo in repos
        if repo.visibility == "PUBLIC"
        and repo.name not in REPOS_PUBLIC_BY_DESIGN
        and repo.active_runs == 0
        and repo.pushed_at <= oldest_young_push
    ]
