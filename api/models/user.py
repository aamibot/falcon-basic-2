from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db import db
from api.models.store import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80))
    password = Column(String(80))

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with db.manager.session_scope() as session:
            session.expire_on_commit = False
            return session.query(UserModel).filter_by(username=username).first()

    def save_to_db(self):
        with db.manager.session_scope() as session:
            session.add(self)
            session.commit()
