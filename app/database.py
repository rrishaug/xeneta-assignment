from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:ratestask@localhost/postgres"

database = SQLAlchemy()
