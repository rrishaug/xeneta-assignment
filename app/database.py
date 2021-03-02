from flask_sqlalchemy import SQLAlchemy

from testcontainers.postgres import PostgresContainer

SQLALCHEMY_DATABASE_URI = None

testing = True

if testing:
    postgres = PostgresContainer("ratestask:latest")
    postgres.start()
    SQLALCHEMY_DATABASE_URI = postgres.get_connection_url()
else:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:ratestask@localhost/postgres"

database = SQLAlchemy()
