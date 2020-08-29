import sqlite3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80))
    password = Column(String(80))


    def __init__(self, _id, username, password):
        super().__init__()
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):

        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE username=?"

            result = cursor.execute(query, (username,))

            row = result.fetchone()

            if row:
                user = cls(*row)
            else:
                user = None     

            return user


