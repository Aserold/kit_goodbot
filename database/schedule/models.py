import datetime
from typing import Annotated

from sqlalchemy import TIME, ForeignKey, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_255 = Annotated[str, 255]


class Base(DeclarativeBase):
    type_annotation_map = {str_255: String(255)}


class Course(Base):
    __tablename__ = "course"

    course_id: Mapped[intpk]
    course_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class Group(Base):
    __tablename__ = "group"

    group_id: Mapped[intpk]
    group_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    course_id: Mapped[int] = mapped_column(
        ForeignKey(Course.course_id, onupdate="CASCADE")
    )


class Weekday(Base):
    __tablename__ = "weekday"

    weekday_id: Mapped[intpk]
    weekday_name: Mapped[str_255]


class Lesson(Base):
    __tablename__ = "lesson"

    lesson_id: Mapped[intpk]
    group_id: Mapped[int] = mapped_column(
        ForeignKey(Group.group_id, onupdate="CASCADE")
    )
    weekday_id: Mapped[int] = mapped_column(
        ForeignKey(Weekday.weekday_id, onupdate="CASCADE")
    )
    start_time: Mapped[datetime.time] = mapped_column(TIME, nullable=False)
    subject: Mapped[str_255] = mapped_column(nullable=False)


schedule_metadata = Base.metadata
