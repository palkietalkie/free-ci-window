# free-ci-window

Opens the free-CI public window for Palkie Talkie's private repos when GitHub refuses their Actions (free minutes spent, or a charge unpaid). Public on purpose: its own Actions are free, so it can act when the private repos cannot. Holds no product code.

- `check_private_ci_is_blocked.py`: whether GitHub will refuse private runs this month. The workspace's pre-push flip and this repo's hourly workflow both read it.
- `.github/workflows/open-free-ci-window.yml`: at :50 each hour, flips the private repos public when blocked, so their :00 crons run. Each repo's `enforce-private.yml` restores private.
