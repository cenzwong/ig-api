import pytest
from unittest.mock import MagicMock
from ig_api.services.markets import MarketService

@pytest.fixture
def mock_api_client():
    client = MagicMock()
    client.request.return_value.json.return_value = {"markets": []}
    return client

def test_get_markets(mock_api_client):
    service = MarketService(mock_api_client)
    epics = ["IX.D.FTSE.DAILY.IP", "KB.D.POWER.DAILY.IP"]
    
    result = service.get_markets(epics)
    
    # Check if request was called correctly
    mock_api_client.request.assert_called_once_with(
        method="GET",
        endpoint="/markets",
        version="2",
        params={"epics": "IX.D.FTSE.DAILY.IP,KB.D.POWER.DAILY.IP"}
    )
    
    assert result == {"markets": []}

def test_search_markets(mock_api_client):
    service = MarketService(mock_api_client)
    search_term = "EURGBP"
    
    mock_api_client.request.return_value.json.return_value = {"markets": [{"epic": "CS.D.EURGBP.TODAY.IP"}]}
    
    result = service.search_markets(search_term)
    
    mock_api_client.request.assert_called_with(
        method="GET",
        endpoint="/markets",
        version="1",
        params={"searchTerm": "EURGBP"}
    )
    
    assert result == {"markets": [{"epic": "CS.D.EURGBP.TODAY.IP"}]}

def test_get_market_by_epic(mock_api_client):
    service = MarketService(mock_api_client)
    epic = "IX.D.FTSE.DAILY.IP"
    
    mock_api_client.request.return_value.json.return_value = {"market": {"epic": "IX.D.FTSE.DAILY.IP"}}
    
    result = service.get_market_by_epic(epic)
    
    mock_api_client.request.assert_called_with(
        method="GET",
        endpoint="/markets/IX.D.FTSE.DAILY.IP",
        version="3"
    )
    
    assert result == {"market": {"epic": "IX.D.FTSE.DAILY.IP"}}
