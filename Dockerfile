FROM python:3.8.0-buster

COPY requirements.txt requirements.txt

RUN python -m venv venv
ENV VIRTUAL_ENV /env
ENV PATH "/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=app/__init__.py

COPY app app
COPY migrations migrations
COPY start-flask-with-migrations start-flask-with-migrations

ENTRYPOINT [ "sh", "start-flask-with-migrations" ]
