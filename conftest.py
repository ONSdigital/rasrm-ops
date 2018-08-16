import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app('DevConfig')
    app.config['BASIC_AUTH_FORCE'] = False
    client = app.test_client()

    yield client
