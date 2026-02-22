from typing import Any
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from app.store.database.sqlalchemy_base import BaseModel


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self.engine: AsyncEngine | None = None
        self._db: type[BaseModel] = BaseModel
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        # Получаем данные из конфига, который уже лежит в app
        cfg = self.app.config.database

        # Собираем URL (обязательно с +asyncpg)
        url = f"postgresql+asyncpg://{cfg.user}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.database}"

        # Создаем движок
        self.engine = create_async_engine(
            url,
            echo=True,  # Полезно для отладки (видит SQL в консоли)
            future=True
        )

        # Создаем фабрику сессий
        self.session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        print("Database connected")

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        if self.engine:
            await self.engine.dispose()
            print("Database disconnected")