from typing import Dict, Any
from ..core.api import ApiClient

class AccountsService:
    """
    Service for managing IG accounts.
    """

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_accounts(self) -> Dict[str, Any]:
        """
        Returns a list of all accounts belonging to the logged-in client.
        
        GET /accounts
        """
        response = self.api_client.request("GET", "/accounts", version="1")
        return response.json()
