from typing import Optional, Any, Self, Dict

from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict

from src.shared.pydantic_schemas.role import RoleSchema


class UserBase(BaseModel):
    email: EmailStr = Field(description='Электронная почта', max_length=256)
    first_name: str = Field(description="Имя", max_length=128)
    middle_name: Optional[str] = Field(description="Отчество", max_length=128, default=None)
    last_name: Optional[str] = Field(description="Фамилия", max_length=128, default=None)

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: Optional[str] = Field(description="Пароль", min_length=8, max_length=64)
    password_confirm: Optional[str] = Field(description="Подтверждение пароля", min_length=8, max_length=64)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def validate(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        password = value.get('password', None)
        password_confirm = value.get('password_confirm', None)
        if not((password and password_confirm) and (password_confirm == password)):
            raise ValueError("Password and confirmation doesn't match. Check password and confirmation again")
        return value

class UserGet(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr = Field(description='Электронная почта', max_length=256)
    password: Optional[str] = Field(description="Пароль", min_length=8, max_length=64)

    model_config = ConfigDict(from_attributes=True)


class UserExtendedSchema(UserGet):
    role_rel: Optional[RoleSchema] = Field(description="Информация о роли", default=None)

    model_config = ConfigDict(from_attributes=True)
