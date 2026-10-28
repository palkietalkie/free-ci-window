# free-ci-window

The clock for Palkie Talkie's scheduled work, and the free-CI public window for its private repos when GitHub refuses their Actions (free minutes spent, or a charge unpaid). Public on purpose: its own Actions are free, so it can act when the private repos cannot. Holds no product code.

- `find_due_workflows.py`: which private-repo workflows run in which UTC hour. The private repos carry no `schedule:` of their own.
- `check_private_ci_is_blocked.py`: whether GitHub will refuse private runs this month. The workspace's pre-push flip and this repo's hourly workflow both read it.
- `.github/workflows/run-scheduled-workflows.yml`: each hour, flips a private repo public when blocked, dispatches what is due, and flips it back once those runs finish. Each repo's `enforce-private.yml` is the safety net that restores private after any other run.
