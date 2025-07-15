from typing import List
from uuid import uuid4


from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.db.base import Base
from  app.db.associative import UserTeamAssoc, Result


class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    private: Mapped[bool] = mapped_column(Boolean())
    users: Mapped[List["User"]] = relationship(secondary=UserTeamAssoc.__tablename__, back_populates="teams", lazy="selectin")
    tournaments: Mapped[List["Tournament"]] = relationship(secondary=Result.__tablename__, back_populates="teams", lazy="selectin")
    
    
    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)