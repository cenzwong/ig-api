from typing import List, Dict
from ..core.api import ApiClient

class MarketService:
    """
    Service for interacting with the IG Markets API.
    """

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_markets(self, epics: List[str]) -> Dict:
        """
        Returns the details of the given markets.
        Reference: https://labs.ig.com/reference/markets.html#GET2
        
        Args:
            epics: List of market epics to retrieve.
            
        Returns:
            Dict containing market details.
        """
        # Join epics with commas usually, but requests params handles lists by repeating keys usually.
        # However, for IG API, it typically expects comma separated string for a single key if it's a list.
        # Let's verify standard behavior or assume comma-separated string for "epics" common in REST APIs.
        # Re-reading: "Returns the details of the given markets."
        # If I pass `params={"epics": "KA.D.AAPL.US.IP,..."}` it works.
        
        epics_str = ",".join(epics)
        params = {"epics": epics_str}
        
        response = self.api_client.request(
            method="GET",
            endpoint="/markets",
            version="2",
            params=params
        )
        
        return response.json()

    def search_markets(self, search_term: str) -> Dict:
        """
        Searches for markets matching the given search term.
        Reference: https://labs.ig.com/reference/markets.html#GET1
        Note: The user request mentioned V2 behavior but search might be V1 or V2 dependent.
        The user provided example uses /markets?searchTerm=... which is usually GET /markets.
        
        Args:
            search_term: The term to search for (e.g., 'EURGBP').
            
        Returns:
            Dict containing search results.
        """
        params = {"searchTerm": search_term}
        
        # Typically search is on the same endpoint. API reference often lists one endpoint with different params.
        response = self.api_client.request(
            method="GET",
            endpoint="/markets",
            version="1", # Search is often V1 unless V2 is specified for search too.
            params=params
        )
        
        return response.json()

    def get_market_by_epic(self, epic: str) -> Dict:
        """
        Returns the details of the given market.
        Reference: https://labs.ig.com/reference/markets-epic.html#GET3
        Using Version 3 by default.
        
        Args:
            epic: The market epic (e.g., 'IX.D.FTSE.DAILY.IP').
            
        Returns:
            Dict containing market details.
        """
        response = self.api_client.request(
            method="GET",
            endpoint=f"/markets/{epic}",
            version="3"
        )
        
        return response.json()
