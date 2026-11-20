from datetime import UTC, datetime

from find_repos_to_make_private import RepoState, find_repos_to_make_private

# The hour these repos were found public, 2026-11-13 22:30 UTC.
NOW = datetime(2026, 11, 13, 22, 30, tzinfo=UTC)


def test_a_repo_left_public_with_nothing_running_is_made_private() -> None:
    # fundraising was flipped on its push of 2026-11-10 and never ran a workflow; ios was flipped on a push after its PR merged, which starts no run, so enforce-private never fired.
    repos = [
        RepoState(name="fundraising", visibility="PUBLIC", pushed_at=datetime(2026, 11, 10, 2, 39, 19, tzinfo=UTC), active_runs=0),
        RepoState(name="ios", visibility="PUBLIC", pushed_at=datetime(2026, 11, 8, 7, 52, 27, tzinfo=UTC), active_runs=0),
    ]

    assert find_repos_to_make_private(repos=repos, now=NOW) == ["fundraising", "ios"]


def test_the_repo_that_is_public_by_design_stays_public() -> None:
    repos = [RepoState(name="free-ci-window", visibility="PUBLIC", pushed_at=datetime(2026, 11, 1, tzinfo=UTC), active_runs=0)]

    assert find_repos_to_make_private(repos=repos, now=NOW) == []


def test_a_window_with_a_run_still_going_stays_open() -> None:
    repos = [RepoState(name="ios", visibility="PUBLIC", pushed_at=datetime(2026, 11, 13, 21, 0, tzinfo=UTC), active_runs=1)]

    assert find_repos_to_make_private(repos=repos, now=NOW) == []


def test_a_window_a_push_opened_moments_ago_stays_open_for_its_runs_to_queue() -> None:
    repos = [RepoState(name="website", visibility="PUBLIC", pushed_at=datetime(2026, 11, 13, 22, 28, tzinfo=UTC), active_runs=0)]

    assert find_repos_to_make_private(repos=repos, now=NOW) == []


def test_a_private_repo_is_left_alone() -> None:
    repos = [RepoState(name="backend", visibility="PRIVATE", pushed_at=datetime(2026, 11, 1, tzinfo=UTC), active_runs=0)]

    assert find_repos_to_make_private(repos=repos, now=NOW) == []
