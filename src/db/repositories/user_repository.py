from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload

from src.db.models import User
from src.shared.pydantic_schemas.user import UserBase, UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, user_data: dict, user_role_id: int):
        new_user = User(**user_data, role_id=user_role_id)
        self.session.add(new_user)
        await self.session.commit()
        return new_user.id

    async def update_one(self, user_id: int, new_data: dict):
        stmt = (update(User)
                .where(
            User.id == user_id,
            User.is_active == True
        )
                .values(**new_data)
                .returning(User)
        )
        user_db = await self.session.execute(stmt)
        await self.session.commit()
        user = user_db.scalars().one_or_none()
        return user

    async def get_by_id(self, user_id: int):
        stmt = (select(User)
                .where(
            User.id == user_id,
            User.is_active == True
        )
                )
        user_db = await self.session.execute(stmt)
        user = user_db.scalars().one_or_none()
        return user

    async def get_all(self):
        stmt = select(User)
        user_db = await self.session.execute(stmt)
        user = user_db.scalars().all()
        return user

    async def get_by_email(self, email: str | EmailStr) -> User:
        stmt = (select(User)
                .where(
            User.email == email,
            User.is_active == True
        )
                )
        user_db = await self.session.execute(stmt)
        user = user_db.scalars().one_or_none()
        return user

    async def get_with_relationships(self, user_id: int):
        stmt = (select(User)
                .where(User.id == user_id)
                .options(
            selectinload(User.role_rel)
        )
        )
        user_db = await self.session.execute(stmt)
        user = user_db.scalars().one_or_none()
        return user