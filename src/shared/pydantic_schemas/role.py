from pydantic import BaseModel, Field, ConfigDict

from src.shared.enum_classes.roles import RoleEnum


class Rights(BaseModel):
    change_users_accounts_status: bool = Field(description='Разрешение на изменение поля "is_active"')
    access_to_protected_resources: bool = Field(description='Разрешение на доступ к защищенным эндпоинтам')


class RoleSchema(Rights):
    id: int
    title: RoleEnum = Field(description="Название роли")

    model_config = ConfigDict(from_attributes=True)