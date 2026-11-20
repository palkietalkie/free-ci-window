from find_due_workflows import SCHEDULES, find_due_workflows


def test_the_morning_reports_and_the_hourly_jobs_fall_due_at_16_utc() -> None:
    due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=16)}
    assert due == {
        "send-scheduled-push-notifications.yml",
        "daily-cost-report.yml",
        "daily-gtm-funnel.yml",
    }


def test_the_push_notifications_fall_due_in_every_hour() -> None:
    for hour in range(24):
        due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=hour)}
        assert "send-scheduled-push-notifications.yml" in due


def test_each_daily_job_falls_due_once_a_day() -> None:
    # The hourly clock fires every hour, so once a day is enough for the database keep-alive too: Aura pauses after 72 idle hours.
    for workflow in ("refresh-daily-content.yml", "keep-free-databases-awake.yml"):
        hours = sum(
            any(s.workflow == workflow for s in find_due_workflows(schedules=SCHEDULES, utc_hour=hour))
            for hour in range(24)
        )
        assert hours == 1, workflow
