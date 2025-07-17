from pydantic import BaseModel


class TeamModel(BaseModel):
    name:str
    private: bool


class TeamModelResponse(TeamModel):
    id: str


