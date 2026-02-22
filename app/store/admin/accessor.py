import hashlib
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

from hashlib import sha256

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        config = app.config.admin
        admin = await self.get_by_email(config.email)

        if not admin:
            await self.create_admin(
                config.email, config.password
            )

    async def get_by_email(self, email: str) -> AdminModel | None:
        async with self.app.database.session() as session:
            query = select(AdminModel).where(AdminModel.email == email)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def create_admin(self, email: str, password: str) -> AdminModel:
        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
        new_admin = AdminModel(email=email, password=hashed_pass)

        async with self.app.database.session() as session:
            session.add(new_admin)
            await session.commit()
            await session.refresh(new_admin)

        return new_admin
