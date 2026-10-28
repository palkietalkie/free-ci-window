from __future__ import annotations

from check_private_ci_is_blocked import ORG
from run_gh import run_gh


def read_visibility(repo: str) -> str:
    return run_gh("repo", "view", f"{ORG}/{repo}", "--json", "visibility", "-q", ".visibility")
