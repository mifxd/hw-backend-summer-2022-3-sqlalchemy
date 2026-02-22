from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.store.database.sqlalchemy_base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)

    question = relationship("QuestionModel", back_populates="theme", cascade="all, delete-orphan")

class QuestionModel(BaseModel):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    theme_id = Column(Integer, ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)

    theme = relationship("ThemeModel", back_populates="question")
    answers = relationship("AnswerModel", back_populates="question", cascade="all, delete-orphan")

class AnswerModel(BaseModel):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    question = relationship("QuestionModel", back_populates="answers")

Theme = ThemeModel
Question = QuestionModel
Answer = AnswerModel