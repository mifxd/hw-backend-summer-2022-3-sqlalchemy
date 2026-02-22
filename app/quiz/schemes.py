from marshmallow import Schema, fields, validates_schema, ValidationError


class ThemeSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True, required=True)

    @validates_schema
    def validate_answers(self, data, **kwargs):
        answers = data.get("answers")

        if not isinstance(answers, list):
            return

        if len(answers) < 2:
            raise ValidationError("Question must have at least 2 answers", field_name="answers")

        correct_count = sum(1 for a in answers if a.get("is_correct") is True)

        if correct_count != 1:
            raise ValidationError("Question must have exactly one correct answer", field_name="answers")


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema(), many=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int(required=True)


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema(), many=True)
