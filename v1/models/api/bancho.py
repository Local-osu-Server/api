from pydantic import BaseModel


class LoginData(BaseModel):
    username: str


class LogoutData(BaseModel):
    user_id: int
