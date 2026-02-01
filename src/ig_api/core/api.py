import requests
from typing import Optional, Dict, Any

class ApiClient:
    """
    Low-level client for handling HTTP requests to the IG API.
    Manages base URL, authentication headers, and error handling.
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.cst: Optional[str] = None
        self.x_security_token: Optional[str] = None

    def _get_headers(self, version: str = "2", auth: bool = False) -> Dict[str, str]:
        """Constructs headers for requests."""
        headers = {
            "X-IG-API-KEY": self.api_key,
            "Version": version,
            "Content-Type": "application/json",
            "Accept": "application/json; charset=UTF-8"
        }
        
        if auth:
            if self.cst:
                headers["CST"] = self.cst
            if self.x_security_token:
                headers["X-SECURITY-TOKEN"] = self.x_security_token
                
        return headers

    def update_tokens(self, cst: Optional[str], x_security_token: Optional[str]):
        """Updates the session tokens."""
        if cst:
            self.cst = cst
        if x_security_token:
            self.x_security_token = x_security_token

    def clear_tokens(self):
        """Clears the session tokens."""
        self.cst = None
        self.x_security_token = None

    def request(self, method: str, endpoint: str, version: str = "1", auth: bool = True, data: Optional[Dict] = None) -> requests.Response:
        """
        Executes an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint (e.g., '/session').
            version: API version for the header.
            auth: Whether to include auth tokens.
            data: JSON payload.
            
        Returns:
            The raw response object.
            
        Raises:
            requests.exceptions.RequestException
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(version=version, auth=auth)
        
        try:
            response = requests.request(method, url, headers=headers, json=data)
            
            # Check for standard HTTP errors (but let caller handle specific logic like 412)
            if not response.ok:
                # We raise here, but services can catch usage-specific errors if needed
                response.raise_for_status()
                
            return response
            
        except requests.exceptions.RequestException as e:
            # We could add centralized logging here
            raise e
