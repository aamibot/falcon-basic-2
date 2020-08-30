from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import db
from api.models.store import Base


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    price = Column(Float(precision=2))

    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("StoreModel")

    def __init__(self, name, price, store_id):
        super().__init__()
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

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
                session.query(ItemModel).filter_by(name=name).first()
            )  # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        with db.manager.session_scope() as session:
            session.add(self)
            session.commit()

    def delete_from_db(self):
        with db.manager.session_scope() as session:
            session.delete(self)
            session.commit()
