import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=None, verbose=False, override=False)


SECRET = os.getenv("JWT_SECRET")
