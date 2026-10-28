from find_due_workflows import SCHEDULES, find_due_workflows


def test_the_morning_reports_and_the_hourly_push_fall_due_at_16_utc() -> None:
    due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=16)}
    assert due == {"send-scheduled-push-notifications.yml", "daily-cost-report.yml", "daily-gtm-funnel.yml"}


def test_the_push_notifications_fall_due_in_every_hour() -> None:
    for hour in range(24):
        due = {schedule.workflow for schedule in find_due_workflows(schedules=SCHEDULES, utc_hour=hour)}
        assert "send-scheduled-push-notifications.yml" in due


def test_a_daily_job_falls_due_once_a_day() -> None:
    days = sum(
        any(s.workflow == "neo4j-keepalive.yml" for s in find_due_workflows(schedules=SCHEDULES, utc_hour=hour))
        for hour in range(24)
    )
    assert days == 1
