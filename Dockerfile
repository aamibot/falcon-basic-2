FROM python:3.7-slim-buster

COPY requirements.txt .

RUN apt-get update \
    && pip install --no-cache-dir -r requirements.txt  \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/* \
    && rm -rf ~/.cache/pip/* \
    && apt-get purge -y --auto-remove \
    && apt-get clean all

WORKDIR /app

ADD . .
    
CMD ["gunicorn", "-c", "python:api.config.gunicorn", "main:api"]