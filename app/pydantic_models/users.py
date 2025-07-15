from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserModelResponse(UserBase):
    id: str
    username: str
    email: str
    is_active: bool
