from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import db

Base = declarative_base()


class StoreModel(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String(80))

    items = relationship(
        "ItemModel", lazy="dynamic", backref="stores"
    )  # Many to one(type-list)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def validate_name(cls, name):
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
            return (
                session.query(StoreModel).filter_by(name=name).first()
            )  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        with db.manager.session_scope() as session:
            session.add(self)
            session.commit()

    def delete_from_db(self):
        with db.manager.session_scope() as session:
            session.delete(self)
            session.commit()
