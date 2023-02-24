FROM python:3.8-slim-buster

ARG default_cors_url="http://localhost:8080"
ARG default_allowed_host="http://localhost:8000"
ARG default_debug=True
ENV CORS_URL=${default_cors_url}\
    ALLOWED_HOST=${default_allowed_host}\
    DEBUG=${default_debug}\
    PYTHONUNBUFFERED=1\
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir application
COPY . /application/
WORKDIR /application

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn","--bind", ":8000", "backend.wsgi"]