#!/usr/bin/env python3
"""Exit 0 when GitHub will refuse to start Actions jobs on the org's private repos this month, exit 1 when they can run. Each repo's pre-push reads the exit code through flip_public_when_private_ci_is_blocked.sh to decide whether to open the public window, where Actions are free.

Two things stop a private run on the Free plan: the 2,000 included minutes running out (Linux x1, macOS x10, Windows x2), and a charge the card on file failed to pay. The second is what counting minutes alone missed on 2026-10-20: 1,984 of October's minutes used, $0.018 of September's storage unpaid, every job refused with "recent account payments have failed". A failure to read the billing API also exits 0, so CI still runs; the public window is brief and enforce-private.yml restores private."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

ORG = "palkietalkie"
ALLOWANCE_MINUTES = 2000
# GitHub weights a runner-minute toward the free quota by OS.
QUOTA_WEIGHTS = {
    "Actions Linux": 1,
    "Actions macOS 3-core": 10,
    "Actions macOS": 10,
    "Actions Windows": 2,
}


def is_private_ci_blocked(*, usage: dict[str, Any], allowance_minutes: int = ALLOWANCE_MINUTES) -> bool:
    """True when this month's Actions minutes have passed the free allowance, or this month or last carries a charge. usage is the org billing-usage payload (untyped external JSON: its usageItems carry each SKU per period).

    Last month counts because a charge is billed after its month ends, so the failed payment that blocks October is September's: on 2026-10-20 October owed nothing and September owed $0.018 for storage. Reading it as blocked when the card actually paid costs one brief public window, while missing it leaves every job unstarted."""
    items = [item for item in usage.get("usageItems", []) if item.get("product") == "actions"]
    periods = sorted({str(item["date"]) for item in items})
    if not periods:
        return False

    this_month = periods[-1]
    if any(float(item.get("netAmount", 0)) > 0 for item in items if item["date"] in periods[-2:]):
        return True

    current = [item for item in items if item["date"] == this_month]

    used_minutes = sum(
        float(item["quantity"]) * QUOTA_WEIGHTS.get(str(item["sku"]), 1)
        for item in current
        if item.get("unitType") == "Minutes"
    )
    return used_minutes >= allowance_minutes


def main() -> int:
    try:
        out = subprocess.run(  # noqa: S603 — fixed `gh` CLI invocation, no untrusted input
            ["gh", "api", f"/organizations/{ORG}/settings/billing/usage"],  # noqa: S607 — `gh` resolved from PATH by design
            capture_output=True,
            text=True,
            timeout=20,
            check=True,
        ).stdout
        is_blocked = is_private_ci_blocked(usage=json.loads(out))
    except Exception:
        return 0

    return 0 if is_blocked else 1


if __name__ == "__main__":
    sys.exit(main())
