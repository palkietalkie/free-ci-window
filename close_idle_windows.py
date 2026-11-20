from __future__ import annotations

import json
from datetime import UTC, datetime

from check_private_ci_is_blocked import ORG
from count_active_runs import count_active_runs
from find_repos_to_make_private import REPOS_PUBLIC_BY_DESIGN, RepoState, find_repos_to_make_private
from run_gh import run_gh
from set_visibility import set_visibility


def close_idle_windows() -> None:
    listed = json.loads(run_gh("repo", "list", ORG, "--json", "name,visibility,pushedAt", "--limit", "200"))
    repos = [
        RepoState(
            name=repo["name"],
            visibility=repo["visibility"],
            pushed_at=datetime.fromisoformat(repo["pushedAt"]),
            # Counting runs costs a call per repo, so only the windows that might be closed are counted.
            active_runs=count_active_runs(repo["name"]) if repo["visibility"] == "PUBLIC" and repo["name"] not in REPOS_PUBLIC_BY_DESIGN else 0,
        )
        for repo in listed
    ]
    for name in find_repos_to_make_private(repos=repos, now=datetime.now(UTC)):
        print(f"{ORG}/{name} is public with nothing running; restoring private")
        set_visibility(name, "private")
