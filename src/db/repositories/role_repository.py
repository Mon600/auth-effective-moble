from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Role, User
from src.shared.enum_classes.roles import RoleEnum
from src.shared.pydantic_schemas.role import Rights


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_user_role_id(self) -> int | None:
        stmt = select(Role.id).where(Role.title == RoleEnum.user.value)
        role_db = await self.session.execute(stmt)
        role_id = role_db.scalars().one_or_none()
        return role_id


    async def create_user_role(self) -> int:
        new_role = Role(title=RoleEnum.user.value)
        self.session.add(new_role)
        await self.session.commit()
        return new_role.id


    async def update_rights(self, role_id: int, new_rights: Rights) -> Role:
        rights_dict = new_rights.model_dump()
        stmt = (update(Role)
                .where(Role.id == role_id)
                .values(**rights_dict)
                .returning(Role)
                )
        role_db = await self.session.execute(stmt)
        await self.session.commit()
        role = role_db.scalars().one_or_none()
        return role


