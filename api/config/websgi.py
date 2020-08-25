# -*- coding: utf-8 -*-

import multiprocessing
import os
from distutils.util import strtobool
from dotenv import load_dotenv

load_dotenv(dotenv_path=None, verbose=False, override=True)

bind = os.getenv("WEB_BIND", f'0.0.0.0:{os.getenv("PORT","8000")}')

accesslog = "-"  #'-' means log to stdout.
access_log_format = (
    "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' in %(D)sµs"
)

workers = int(os.getenv("WEB_CONCURRENCY"))
worker_tmp_dir = os.getenv("WORKER_TMP_DIR")

threads = int(os.getenv("PYTHON_MAX_THREADS"))

reload = bool(strtobool(os.getenv("WEB_RELOAD")))
