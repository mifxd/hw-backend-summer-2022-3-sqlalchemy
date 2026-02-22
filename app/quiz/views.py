from app.quiz.models import Answer
from app.quiz.schemes import ThemeSchema, ThemeListSchema, QuestionSchema, ThemeIdSchema, ListQuestionSchema
from app.web.app import View
from app.web.utils import json_response, error_json_response
from marshmallow import ValidationError


class ThemeAddView(View):
    async def post(self):
        admin = self.request.admin
        if not admin:
            return error_json_response(401, status="unauthorized",
                                       message="Only admins can create themes")

        data = await self.request.json()
        valid_data = ThemeSchema().load(data)
        title = valid_data["title"]

        theme_exist = await self.store.quizzes.get_theme_by_title(title)
        if theme_exist:
            return error_json_response(409, status="conflict",
                                       message="Theme already exists")

        new_theme = await self.store.quizzes.create_theme(title=title)

        response = ThemeSchema().dump(new_theme)
        return json_response(data=response)


class ThemeListView(View):
    async def get(self):
        admin = self.request.admin
        if not admin:
            return error_json_response(401, status="unauthorized",
                                       message="Only admins can view themes")

        themes = await self.store.quizzes.list_themes()

        response = ThemeListSchema().dump({"themes": themes})
        return json_response(data=response)


class QuestionAddView(View):
    async def post(self):
        admin = self.request.admin
        if not admin:
            return error_json_response(401, status="unauthorized",
                                       message="Only admins can create themes")

        try:
            raw_data = await self.request.json()
            data = QuestionSchema().load(raw_data)
        except ValidationError as e:
            import sys
            print(f"\n!!! ОШИБКА СХЕМЫ: {e.messages}\n", file=sys.stderr)

            return error_json_response(http_status=400,
                                       status="bad_request",
                                       data=e.messages)

        title = data["title"]
        theme_id = data["theme_id"]
        answers = [Answer(title=a["title"], is_correct=a["is_correct"]) for a in data["answers"]]

        theme_exist = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme_exist:
            return error_json_response(404, status="not_found",
                                       message="Theme not found")

        existing_question = await self.store.quizzes.get_question_by_title(title)
        if existing_question:
            return error_json_response(409, status="conflict", message="Question already exists")

        question = await self.store.quizzes.create_question(
            title=title, theme_id=theme_id, answers=answers
        )
        return json_response(data=QuestionSchema().dump(question))

class QuestionListView(View):
    async def get(self):
        admin = self.request.admin
        if not admin:
            return error_json_response(401, status="unauthorized",
                                       message="Only admins can view questions")

        raw_params = self.request.query
        try:
            params = ThemeIdSchema().load(raw_params)
        except ValidationError:
            params = {}

        theme_id = params.get("theme_id")
        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(data=ListQuestionSchema().dump({"questions": questions}))