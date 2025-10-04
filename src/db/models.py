from email.policy import default
from typing import Optional, List

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.shared.enum_classes.roles import RoleEnum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(128), index=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(128), index=True, nullable=True)
    middle_name: Mapped[Optional[str]] = mapped_column(String(128), index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete="SET NULL"), nullable=True)
    role_rel: Mapped["Role"] = relationship(back_populates='users_rel')


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement=True)
    title: Mapped[str] = mapped_column(Enum(RoleEnum, name='roles_enum'), unique=True)
    access_to_protected_resources: Mapped[bool] = mapped_column(default=False)
    users_rel: Mapped["User"] = relationship()
