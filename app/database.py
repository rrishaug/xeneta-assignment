import sys

from flask_sqlalchemy import SQLAlchemy

from testcontainers.postgres import PostgresContainer

SQLALCHEMY_DATABASE_URI = None

# somewhat hacky setup to run a testcontainer when running tests
testing = "pytest" in sys.modules
postgres_container = None

def stop_postgres_container():
    if postgres_container != None:
        postgres_container.stop()

if testing:
    postgres_container = PostgresContainer("ratestask-db:latest")
    postgres_container.start()
    SQLALCHEMY_DATABASE_URI = postgres_container.get_connection_url()
else:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:ratestask@localhost/postgres"

database = SQLAlchemy()
