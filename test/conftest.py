import os

os.environ['OPEN_EX_RATES_API_KEY'] = 'DUMMY_API_KEY'

import pytest

from app import create_app
from app.database import database, stop_postgres_container

@pytest.fixture
def app():
    test_app = create_app()
    return test_app

# TODO reset db between tests, could submodule the ratestask repo. Then truncate db between tests and use the .sql file to restore initial state
@pytest.fixture()
def database():
    return database

@pytest.fixture
def rest_client(app):
    return app.test_client()

def pytest_unconfigure(config):
    stop_postgres_container()