from sqlalchemy import Column, Integer, String
from app.store.database.sqlalchemy_base import BaseModel
from hashlib import sha256


class AdminModel(BaseModel):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def is_password_valid(self, password: str) -> bool:
        # Хешируем входящий пароль и сравниваем с тем, что в базе
        return self.password == sha256(password.encode()).hexdigest()

Admin = AdminModel