from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.config import settings
from app.pydantic_models.token import TokenModel
from app.pydantic_models.users import UserModel, UserModelResponse
from app.db.users import db_actions
from app.db.users.models import User


users_route = APIRouter(prefix="/users", tags=["User"])


async def get_users_id(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/users/token/"))]) -> str:
    try:
        payload: Dict = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user_id

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@users_route.post("/", status_code=status.HTTP_201_CREATED, summary="Create user")
async def sign_up(user_model: UserModel, db: Annotated[AsyncSession, Depends(get_db)]):
    await db_actions.sign_up(user_model=user_model, db=db)


@users_route.post("/token/", status_code=status.HTTP_202_ACCEPTED, response_model=TokenModel, summary="Login")
async def sign_in(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]) -> TokenModel:
    token = await db_actions.sign_in(username=form.username, password=form.password, db=db)
    return dict(access_token=token)


@users_route.get("/", status_code=status.HTTP_202_ACCEPTED, response_model=UserModelResponse, summary="Get user")
async def get_me(user_id: Annotated[str, Depends(get_users_id)], db: Annotated[AsyncSession, Depends(get_db)]) -> User:
    return await db_actions.get_user(user_id=user_id, db=db)