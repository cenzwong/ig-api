import pytest
import os
from unittest.mock import MagicMock
from ig_api.client import IGClient

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("IG_API_KEY", "test_key")
    monkeypatch.setenv("IG_USERNAME", "test_user")
    monkeypatch.setenv("IG_PASSWORD", "test_pass")
    monkeypatch.setenv("IG_ENV", "demo")

@pytest.fixture
def client(mock_env):
    return IGClient()

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.headers = {}
    mock.json.return_value = {}
    mock.raise_for_status.return_value = None
    return mock
