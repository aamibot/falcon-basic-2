import os
from sqlalchemy import create_engine
import falcon_sqla


def get_url():
    return os.getenv("DATABASE_URL", "sqlite:///data.db")

class SessionScope(object):
    def __init__(self):
        super().__init__()
        self.engine = create_engine(get_url())
        self.manager = falcon_sqla.Manager(self.engine)

db = SessionScope()