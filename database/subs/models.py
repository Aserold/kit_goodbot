from typing import Annotated
import datetime

from sqlalchemy import String, SmallInteger, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_255 = Annotated[str, 255]


class Base(DeclarativeBase):
    type_annotation_map = {str_255: String(255)}


class Schedule(Base):
    __tablename__ = 'schedule'

    schedule_id: Mapped[intpk]
    day: Mapped[str_255]
    date: Mapped[datetime.date] = mapped_column(Date)


class Lecture(Base):
    __tablename__ = 'lecture'

    lecture_id: Mapped[intpk]
    schedule_id: Mapped[int] = mapped_column(ForeignKey(Schedule.schedule_id))
    group_name: Mapped[str_255]
    lecture_number: Mapped[int] = mapped_column(SmallInteger)
    subject: Mapped[str_255]
    substitute_teacher: Mapped[str_255]
    new_subject: Mapped[str_255]
    classroom: Mapped[str_255]


subs_metadata = Base.metadata
