import pytest
from unittest.mock import MagicMock
from ig_api.client import IGClient
from ig_api.core.api import ApiClient
from ig_api.services.session import SessionService

def test_init_structure(client):
    assert isinstance(client.api_client, ApiClient)
    assert isinstance(client.session, SessionService)
    assert client.api_client.base_url == "https://demo-api.ig.com/gateway/deal"

def test_connect_delegation(client):
    # Setup mock
    client.session.create = MagicMock(return_value={"cst": "test_cst"})
    
    # Execute
    result = client.connect()
    
    # Assert
    assert result == {"cst": "test_cst"}
    client.session.create.assert_called_once_with("test_user", "test_pass")

def test_logout_delegation(client):
    client.session.delete = MagicMock(return_value=True)
    assert client.logout() is True
    client.session.delete.assert_called_once()
