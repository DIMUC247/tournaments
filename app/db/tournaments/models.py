from uuid import uuid4
from typing import List
from datetime import date, timedelta, datetime, timezone


from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.db.base import Base
from app.db.associative import Result


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    expire_date: Mapped[date] = mapped_column(Date())
    teams: Mapped[List["Team"]] = relationship(secondary=Result.__tablename__, back_populates="tournaments", lazy="selectin")

    def __init__(self, exp_days: int=7, **kwargs):
        self.id = uuid4().hex
        self.expire_date = date.today(timezone.utc) + timedelta(days=exp_days)
        super().__init__(**kwargs)

