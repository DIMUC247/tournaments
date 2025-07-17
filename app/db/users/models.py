from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import bcrypt
import jwt

from app.db.base import Base
from app.config import settings
from app.db.associative import UserTeamAssoc


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    teams: Mapped[List["Team"]] = relationship(lazy="selectin", back_populates="users", secondary=UserTeamAssoc.__tablename__)


    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, pwd: str):
        self.password_ = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

    def is_verify_password(self, pwd: str):
        return bcrypt.checkpw(pwd.encode(), self.password_.encode())

    def get_token(self, pwd: str, expire_time_minutes: int = settings.exp_time_minutes) -> str:
        if not self.is_verify_password(pwd):
            return

        payload = dict(sub=self.id, exp=datetime.now(timezone.utc) + timedelta(minutes=expire_time_minutes))
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm="HS256")
