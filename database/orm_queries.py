import asyncio
import datetime

from sqlalchemy import select, update, text

from models import Course, Group, Weekday, Lesson
from database import async_session
from parser.schedule import parse_schedule

WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
COURSES = [1, 2, 3, 4]
GROUPS = {
    1: [131, 132, 133, 134, 135, 136, 137, 31, 32],
    2: [221, 222, 223, 224, 225, 226, 227, 21, 22],
    3: [311, 312, 313, 314, 315, 316, 11, 12],
    4: [401, 402, 403, 404, 405, 406]
}


async def add_schedule(session, data: list[dict, ...]):
    async with session() as session:
        # Это проверка на наличие записей в таблицах: Weekday, Course, Group
        check_query_weekday = select(Weekday)
        result_weekday = await session.execute(check_query_weekday)
        if not result_weekday.scalars().all():
            for day in WEEKDAYS:
                add_week = Weekday(weekday_name=day)
                session.add(add_week)
                await session.commit()
        check_query_course = select(Course)
        result_course = await session.execute(check_query_course)
        if not result_course.scalars().all():
            for course in COURSES:
                add_course = Course(course_number=course)
                session.add(add_course)
                await session.commit()
        check_query_group = select(Group)
        result_group = await session.execute(check_query_group)
        if not result_group.scalars().all():
            for course, group_list in GROUPS.items():
                for group in group_list:
                    add_group = Group(course_id=course, group_number=group)
                    session.add(add_group)
                    await session.commit()
        # Начинаем танцы с бубном (запись предметов в таблицу)
        await session.execute(text('TRUNCATE TABLE lesson RESTART IDENTITY CASCADE'))  # Очищаем таблицу
        await session.commit()
        for lesson in data:
            # Получаем идентификатор группы запросом
            group_id_query = select(Group.group_id).where(Group.group_number == lesson['group'])
            result_group_id = await session.execute(group_id_query)
            group_id = result_group_id.scalar()
            # Получаем остальные данные из данных парсера
            weekday_id = lesson['day']
            start_time_formatted = lesson['time'].split(':')  # Так как данные приходят строкой по типу "9:00", обрежем
            # Делаем время в формате datetime.time
            start_time = datetime.time(hour=int(start_time_formatted[0]), minute=int(start_time_formatted[1]))
            subject = lesson['lesson']
            add_lesson = Lesson(group_id=group_id, weekday_id=weekday_id, start_time=start_time, subject=subject)
            session.add(add_lesson)
            await session.commit()


# asyncio.run(add_schedule(session=async_session, data=parse_schedule()))
