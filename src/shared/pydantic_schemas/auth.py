from pydantic import BaseModel

from src.db.models import User
from src.shared.pydantic_schemas.user import UserBase


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RegisterResponse(TokenResponse):
    user_id: int


class LoginResponse(TokenResponse):
    user: UserBase
