import pytest
from fastapi.testclient import TestClient

from fastapi_zero.app import app


@pytest.fixture(scope='module')
def client():
    return TestClient(app)
