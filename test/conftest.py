import pytest

from app import create_app
from app.database import database, stop_postgres_container

@pytest.fixture
def app():
    test_app = create_app()
    # test_ctx = test_app.test_request_context()
    # test_ctx.push()
    return test_app

@pytest.fixture(autouse=True)
def database():
    return database

@pytest.fixture
def rest_client(app):
    return app.test_client()

def pytest_unconfigure(config):
    stop_postgres_container()