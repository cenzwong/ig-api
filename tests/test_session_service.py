import pytest
from unittest.mock import MagicMock
from ig_api.core.api import ApiClient
from ig_api.services.session import SessionService

@pytest.fixture
def api_client():
    return MagicMock(spec=ApiClient)

@pytest.fixture
def session_service(api_client):
    return SessionService(api_client)

def test_session_create(session_service, api_client):
    # Setup
    mock_response = MagicMock()
    mock_response.headers = {"CST": "cst1", "X-SECURITY-TOKEN": "xst1"}
    mock_response.json.return_value = {"currentAccountId": "ACC1"}
    api_client.request.return_value = mock_response
    
    # Execute
    result = session_service.create("user", "pass")
    
    # Assert
    api_client.request.assert_called_with("POST", "/session", version="2", auth=False, data={"identifier": "user", "password": "pass"})
    api_client.update_tokens.assert_called_with("cst1", "xst1")
    assert session_service.account_id == "ACC1"
    assert result["cst"] == "cst1"

def test_session_read(session_service, api_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"clientId": "123"}
    api_client.request.return_value = mock_response
    
    result = session_service.read()
    
    assert result["clientId"] == "123"
    api_client.request.assert_called_with("GET", "/session", version="1")

def test_switch_account(session_service, api_client):
    mock_response = MagicMock()
    mock_response.headers = {}
    api_client.request.return_value = mock_response
    api_client.cst = "cst_old"
    api_client.x_security_token = "xst_old"
    
    result = session_service.switch_account("ACC_NEW")
    
    api_client.request.assert_called_with("PUT", "/session", version="1", data={"accountId": "ACC_NEW", "defaultAccount": False})
    assert session_service.account_id == "ACC_NEW"
