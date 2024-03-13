import datetime
import re

from sqlalchemy import func, select, text

from database.schedule.models import Course, Group, Lesson, Weekday
from database.subs.models import Lecture, Schedule

WEEKDAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
COURSES = [1, 2, 3, 4]
GROUPS = {
    1: [131, 132, 133, 134, 135, 136, 137, 31, 32],
    2: [221, 222, 223, 224, 225, 226, 227, 21, 22],
    3: [311, 312, 313, 314, 315, 316, 11, 12],
    4: [401, 402, 403, 404, 405, 406],
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
        await session.execute(
            text("TRUNCATE TABLE lesson RESTART IDENTITY CASCADE")
        )  # Очищаем таблицу
        await session.commit()
        for lesson in data:
            # Получаем идентификатор группы запросом
            group_id_query = select(Group.group_id).where(
                Group.group_number == lesson["group"]
            )
            result_group_id = await session.execute(group_id_query)
            group_id = result_group_id.scalar()
            # Получаем остальные данные из данных парсера
            weekday_id = lesson["day"]
            start_time_formatted = lesson["time"].split(
                ":"
            )  # Так как данные приходят строкой по типу "9:00", обрежем
            # Делаем время в формате datetime.time
            start_time = datetime.time(
                hour=int(start_time_formatted[0]),
                minute=int(start_time_formatted[1])
            )
            subject = lesson["lesson"]
            add_lesson = Lesson(
                group_id=group_id,
                weekday_id=weekday_id,
                start_time=start_time,
                subject=subject,
            )
            session.add(add_lesson)
            await session.commit()


async def get_schedule(session, group: int):
    async with session() as session:
        query = (
            select(Weekday.weekday_name, Lesson.start_time, Lesson.subject)
            .join(Group, Lesson.group_id == Group.group_id)
            .join(Weekday, Lesson.weekday_id == Weekday.weekday_id)
            .where(Group.group_number == group)
        )
        result = await session.execute(query)
        schedule = result.fetchall()
        sorted_schedule = sorted(
            schedule, key=lambda x: (WEEKDAYS.index(x[0]), x[1])
        )
        return sorted_schedule


async def add_subs(session, data: list[dict, ...]):
    day = data[0]["day"]
    raw_date = data[1]["date"].split(".")
    date = datetime.date(
        day=int(raw_date[0]),
        month=int(raw_date[1]),
        year=int(f"20{raw_date[2]}")
    )
    async with session() as session:
        await session.execute(
            text("TRUNCATE TABLE schedule, lecture RESTART IDENTITY CASCADE")
        )  # Очищаем таблицу
        await session.commit()
        add_subschedule = Schedule(day=day, date=date)
        session.add(add_subschedule)
        await session.commit()
        for sub in data[2:]:
            group_name = sub["group"]
            lectures = sub["lectures"]

            for lecture in lectures:
                lecture_number: str = lecture["lecture_number"]
                try:
                    subject = lecture["subject"]
                    substitute_teacher = lecture["substitute_teacher"]
                    new_subject = lecture["new_subject"]
                    classroom = lecture["classroom"]

                    add_sublesson = Lecture(
                        group_name=group_name,
                        lecture_number=int(lecture_number),
                        subject=subject,
                        substitute_teacher=substitute_teacher,
                        new_subject=new_subject,
                        classroom=classroom,
                    )
                    session.add(add_sublesson)
                    await session.commit()
                except ValueError:
                    lecture_1 = int(lecture_number.split(",")[0])
                    lecture_2 = int(lecture_number.split(",")[-1])
                    subject = lecture["subject"]
                    substitute_teacher = lecture["substitute_teacher"]
                    new_subject = lecture["new_subject"]
                    classroom = lecture["classroom"]

                    add_sublesson1 = Lecture(
                        group_name=group_name,
                        lecture_number=lecture_1,
                        subject=subject,
                        substitute_teacher=substitute_teacher,
                        new_subject=new_subject,
                        classroom=classroom,
                    )
                    session.add(add_sublesson1)
                    await session.commit()
                    add_sublesson2 = Lecture(
                        group_name=group_name,
                        lecture_number=lecture_2,
                        subject=subject,
                        substitute_teacher=substitute_teacher,
                        new_subject=new_subject,
                        classroom=classroom,
                    )
                    session.add(add_sublesson2)
                    await session.commit()


async def check_for_subs(session, group: int):
    async with session() as session:
        query = select(Lecture.group_name)
        result = await session.execute(query)
        exclusive_result = [
            re.findall(r"\d+", group_num)[0]
            for group_num in set(result.scalars().all())
        ]
        if str(group) in exclusive_result:
            return True
        return False


async def get_subs(session, group: int):
    async with session() as session:
        group_filter = f"^{group}[a-z]?$"
        query = (
            select(Lecture)
            .where(func.lower(Lecture.group_name).op("~")(group_filter))
            .order_by(Lecture.lecture_number)
        )
        result = await session.execute(query)
        subs = result.scalars().all()
        day_res = await session.execute(select(Schedule.day))
        day = day_res.scalars().first()
        date_res = await session.execute(select(Schedule.date))
        date = date_res.scalars().first()

        lectures_list = [{"day": day}, {"date": date}]

        for lecture in subs:
            lecture_dict = {
                "lecture_number": lecture.lecture_number,
                "subject": lecture.subject,
                "substitute_teacher": lecture.substitute_teacher,
                "new_subject": lecture.new_subject,
                "classroom": lecture.classroom,
            }
            lectures_list.append(lecture_dict)

        return lectures_list
