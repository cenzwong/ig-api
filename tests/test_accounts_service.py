import pytest
from unittest.mock import MagicMock
from ig_api.core.api import ApiClient
from ig_api.services.accounts import AccountsService

@pytest.fixture
def api_client():
    return MagicMock(spec=ApiClient)

@pytest.fixture
def accounts_service(api_client):
    return AccountsService(api_client)

def test_get_accounts(accounts_service, api_client):
    # Setup
    mock_response = MagicMock()
    mock_response.json.return_value = {"accounts": [{"accountId": "ACC1"}, {"accountId": "ACC2"}]}
    api_client.request.return_value = mock_response
    
    # Execute
    result = accounts_service.get_accounts()
    
    # Assert
    api_client.request.assert_called_with("GET", "/accounts", version="1")
    assert len(result["accounts"]) == 2
    assert result["accounts"][0]["accountId"] == "ACC1"
