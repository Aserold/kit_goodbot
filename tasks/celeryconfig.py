from celery.schedules import crontab

broker_url = "redis://localhost:6378/1"
timezone = "UTC"

beat_schedule = {
    "schedule-hourly-update": {
        "task": "tasks.tasks.hourly_schedule_update",
        "schedule": crontab(minute=[0], hour="*"),
    },
    "subs-hourly-update": {
        "task": "tasks.tasks.hourly_subs_update",
        "schedule": crontab(minute=[0], hour="*"),
    },
}
