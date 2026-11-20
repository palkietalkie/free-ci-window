from find_due_workflows import SCHEDULES, find_due_workflows


def test_the_morning_reports_and_the_hourly_jobs_fall_due_at_16_utc() -> None:
    due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=16)}
    assert due == {
        "send-scheduled-push-notifications.yml",
        "keep-free-databases-awake.yml",
        "daily-cost-report.yml",
        "daily-gtm-funnel.yml",
    }


def test_the_push_notifications_fall_due_in_every_hour() -> None:
    for hour in range(24):
        due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=hour)}
        assert "send-scheduled-push-notifications.yml" in due


def test_a_daily_job_falls_due_once_a_day() -> None:
    days = sum(
        any(s.workflow == "refresh-daily-content.yml" for s in find_due_workflows(schedules=SCHEDULES, utc_hour=hour))
        for hour in range(24)
    )
    assert days == 1


def test_the_database_keep_alive_falls_due_every_hour() -> None:
    # This clock fires about three times a day at hours GitHub picks, so a keep-alive due in one hour ran on the days a run happened to land in it: Nov 3, 5, 9 and 11, and the prd graph paused after Aura's 72 idle hours (2026-11-20).
    for hour in range(24):
        due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=hour)}
        assert "keep-free-databases-awake.yml" in due
