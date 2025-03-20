from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    password: str
