import asyncio
from parser.schedule import parse_schedule
from parser.substitutes import parse_subs

from celery import Celery

from database.database import async_session
from database.orm_queries import add_schedule, add_subs

app = Celery("tasks", broker="redis://localhost:6378/1")
app.config_from_object("tasks.celeryconfig")


@app.task
def hourly_schedule_update():
    data = parse_schedule()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(add_schedule(async_session, data))
    return result


@app.task
def hourly_subs_update():
    data = parse_subs()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(add_subs(async_session, data))
    return result


# hourly_schedule_update.delay()
# hourly_subs_update.delay()
