from __future__ import annotations

from check_private_ci_is_blocked import ORG
from run_gh import run_gh


def set_visibility(repo: str, visibility: str) -> None:
    run_gh("repo", "edit", f"{ORG}/{repo}", "--visibility", visibility, "--accept-visibility-change-consequences")
