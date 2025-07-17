from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.users.models import User
from app.pydantic_models.users import UserModel


async def get_user(user_id: str, db: AsyncSession) -> Optional[User]:
    query = select(User).filter_by(id=user_id)
    return await db.scalar(query)


async def sign_up(user_model: UserModel, db: AsyncSession) -> None:
    user = User(**user_model.model_dump())
    db.add(user)
    await db.commit()


async def sign_in(username: str, password: str, db: AsyncSession) -> Optional[str]:
    user: Optional[User] = await db.scalar(select(User).filter_by(username=username))
    if user:
        return user.get_token(pwd=password)

