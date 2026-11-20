# free-ci-window

The clock for Palkie Talkie's scheduled work, and the free-CI public window for its private repos when GitHub refuses their Actions (free minutes spent, or a charge unpaid). Public on purpose: its own Actions are free, so it can act when the private repos cannot. Holds no product code.

- `find_due_workflows.py`: which private-repo workflows run in which UTC hour. The private repos carry no `schedule:` of their own.
- `check_private_ci_is_blocked.py`: whether GitHub will refuse private runs this month. The workspace's pre-push flip and this repo's hourly workflow both read it.
- `.github/workflows/run-scheduled-workflows.yml`: each hour, flips a private repo public when blocked, dispatches what is due, and flips it back once those runs finish. Each repo's `enforce-private.yml` is the safety net that restores private after any other run.
- `close_idle_windows.py`: each hour, first, makes private any repo left public with nothing running. `enforce-private.yml` fires only when another run completes, so a flip that starts no run (a push after its PR merged, as `ios` on 2026-11-08) left the repo public until this caught it.
