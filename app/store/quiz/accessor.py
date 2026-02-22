from collections.abc import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        new_theme = ThemeModel(title=title)

        async with self.app.database.session() as session:
            session.add(new_theme)
            await session.commit()
            await session.refresh(new_theme)

        return new_theme

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        async with self.app.database.session() as session:
            query = select(ThemeModel).where(ThemeModel.title == title)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        async with self.app.database.session() as session:
            query = select(ThemeModel).where(ThemeModel.id == id_)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def list_themes(self) -> Sequence[ThemeModel]:
        async with self.app.database.session() as session:
            query = select(ThemeModel)
            result = await session.execute(query)

            return result.scalars().all()

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        new_question = QuestionModel(title=title, theme_id=theme_id, answers=answers)

        async with self.app.database.session() as session:
            session.add(new_question)
            await session.commit()

        return await self.get_question_by_title(title)

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        async with self.app.database.session() as session:
            query = (
                select(QuestionModel)
                .where(QuestionModel.title == title)
                .options(joinedload(QuestionModel.answers))
            )
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        async with self.app.database.session() as session:
            query = select(QuestionModel).options(joinedload(QuestionModel.answers))
            if theme_id:
                query = query.where(QuestionModel.theme_id == theme_id)

            result = await session.execute(query)

            return result.scalars().unique().all()
