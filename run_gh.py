from __future__ import annotations

import os
import subprocess


def run_gh(*args: str, token: str | None = None) -> str:
    """`token` is for the one call the admin token cannot make; None runs with GH_TOKEN, the admin token that changes visibility."""
    env = {**os.environ, "GH_TOKEN": token} if token else None
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True, env=env).stdout.strip()  # noqa: S603, S607 — fixed `gh` invocation
