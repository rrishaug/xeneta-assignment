import os

os.environ['OPEN_EX_RATES_API_KEY'] = 'DUMMY_API_KEY'

import pytest

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from app import create_app
from app.database import database, stop_postgres_container

@pytest.fixture(scope='session')
def app():
    test_app = create_app()

    ctx = test_app.test_request_context()
    ctx.push()

    alembic_config = AlembicConfig('migrations/alembic.ini')
    alembic_config
    alembic_upgrade(alembic_config, 'head')

    def teardown():
        ctx.pop()

    return test_app

# TODO reset db between tests, could submodule the ratestask repo. Then truncate db between tests and use the .sql file to restore initial state
@pytest.fixture(scope='session', autouse=True)
def database(app):
    return database

@pytest.fixture(scope='session')
def rest_client(app):
    return app.test_client()

def pytest_unconfigure(config):
    stop_postgres_container()