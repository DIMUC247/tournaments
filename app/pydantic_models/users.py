from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: str
    password: str


class UserModelResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
