import sqlite3
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from db import db

Base = declarative_base()

class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    price = Column(Float(precision=2))

    def __init__(self, name, price):
        super().__init__()
        self.name = name
        self.price = price

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def validate_name(cls,name):
        "Check type of name"
        if not name:
            return True
        else:
            try:
                float(name)
                return True
            except ValueError:
                return False

    @classmethod
    def find_by_name(cls, name) -> object:
        with db.manager.session_scope() as session:
            session.expire_on_commit = False
            return session.query(ItemModel).filter_by(name=name).first() #SELECT * FROM items WHERE name=name LIMIT 1
            
    def save_to_db(self):
        with db.manager.session_scope() as session:
            session.add(self)
            session.commit()

    def delete_from_db(self):
        with db.manager.session_scope() as session:
            session.delete(self)
            session.commit()