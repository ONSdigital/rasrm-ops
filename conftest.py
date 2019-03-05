import pytest
from requests.auth import _basic_auth_str

from app import create_app


@pytest.fixture
def client():
    app = create_app('DevelopmentConfig')
    client = app.test_client()

    old_open = client.open

    def open_with_auth(*args, **kwargs):
        kwargs['headers'] = kwargs.get('headers') or {}
        kwargs['headers']['Authorization'] = _basic_auth_str('admin', 'secret')
        return old_open(*args, **kwargs)
    client.open = open_with_auth

    yield client
