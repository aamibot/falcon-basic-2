import os
from sqlalchemy import create_engine
import falcon_sqla
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from dotenv import load_dotenv

load_dotenv(dotenv_path=None, verbose=False, override=True)


def get_url():
    return os.getenv("DATABASE_URL")


class SessionScope(object):
    def __init__(self):
        super().__init__()
        self.engine = create_engine(get_url())
        self.manager = falcon_sqla.Manager(self.engine)


db = SessionScope()
meta = MetaData(db.engine)

if not db.engine.dialect.has_table(connection=db.engine, table_name='users'):
    
    # Register t1, t2, t3 to metadata
    t1 = Table(
        "users",
        meta,
        Column("id", Integer, primary_key=True),
        Column("username", String(80)),
        Column("password", String(80)),
    )

    t2 = Table(
        "stores", meta, Column("id", Integer, primary_key=True), Column("name", String(80))
    )

    t3 = Table(
        "items",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", String(80)),
        Column("price", Float(precision=2)),
        Column("store_id", Integer, ForeignKey("stores.id")),
    )

    meta.create_all(checkfirst=True)
