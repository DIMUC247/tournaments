from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.associative import UserTeamAssoc,Result, Role
from app.db.teams.models import Team
from app.pydantic_models.teams import TeamModel
from app.db.users.models import User
from app.db.users.db_actions import get_user


async def create_team(user_id: str, team_model:TeamModel,db: AsyncSession)-> None:
    team = Team(team_model.model_dump())
    user_team_assoc = UserTeamAssoc(user_id=user_id, team=team, role=Role.teamlead)
    db.add(user_team_assoc)
    await db.commit()


async def get_team(team_id: str, db: AsyncSession) -> Optional[Team]:
    return await db.scalar(select(Team).filter_by(id=team_id))


async def get_teams(private: Optional[bool], db: AsyncSession) -> List[Team]:
    if private is not None:
        return await db.scalars(Team)
    else:
        return await db.scalars(select(Team).filter_by(private=private))
    

async def remove_team(team_id: str, user_id: str, db: AsyncSession) -> bool:
    team= await db.scalar(select(UserTeamAssoc).filter_by(Team.id==team_id, User.id==user_id,UserTeamAssoc.role==Role.teamlead))
    if not team:
        return False

    db.delete(team)
    await db.commit()
    return True


async def add_user_by_team_lead(team_id: str, user_id: str, member_user_id: str, db: AsyncSession) -> bool:
    team: Optional[Team] = await db.scalar(select(UserTeamAssoc).filter_by(Team.id==team_id, User.id==user_id,UserTeamAssoc.role==Role.teamlead))
    user: Optional[User] = await get_user(user_id=member_user_id, db=db)
    if not team or not user:
        return False

    team.users.append(user)
    await db.commit()
    return True


async def add_user_to_team(team_id:str, user_id: str, db: AsyncSession) -> bool:
    team = await db.scalar(select(Team).filter_by(id=team_id,private=False))
    if not team:
        return False

    user: User = await get_user(user_id=user_id, db=db)
    team.users.append(user)
    await db.commit()
    return True