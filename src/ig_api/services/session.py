from typing import Dict, Optional, Any
import requests
from ..core.api import ApiClient

class SessionService:
    """
    Service for managing IG API sessions (login, switch, logout).
    """

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.account_id: Optional[str] = None

    def create(self, username: str, password: str) -> Dict[str, Any]:
        """
        Logs in and creates a session (POST /session v2).
        """
        data = {
            "identifier": username,
            "password": password
        }
        
        response = self.api_client.request("POST", "/session", version="2", auth=False, data=data)
        
        # Extract and update tokens
        cst = response.headers.get("CST")
        xst = response.headers.get("X-SECURITY-TOKEN")
        self.api_client.update_tokens(cst, xst)
        
        resp_json = response.json()
        self.account_id = resp_json.get("currentAccountId") or resp_json.get("accountId")
        
        return {
            "cst": cst,
            "x_security_token": xst,
            "account_id": self.account_id,
            "details": resp_json
        }

    def read(self) -> Dict[str, Any]:
        """
        Gets details of the current session (GET /session).
        """
        response = self.api_client.request("GET", "/session", version="1")
        return response.json()

    def switch_account(self, account_id: str) -> Dict[str, Any]:
        """
        Switches the active account (PUT /session).
        """
        data = {
            "accountId": account_id,
            "defaultAccount": False
        }
        
        try:
            response = self.api_client.request("PUT", "/session", version="1", data=data)
            
            # Update tokens if changed
            cst = response.headers.get("CST")
            xst = response.headers.get("X-SECURITY-TOKEN")
            if cst or xst:
                self.api_client.update_tokens(cst, xst)
                
            self.account_id = account_id
            
            return {
                "cst": self.api_client.cst,
                "x_security_token": self.api_client.x_security_token,
                "account_id": self.account_id
            }
            
        except requests.exceptions.HTTPError as e:
             # Handle "Same Account" error (412)
            if e.response.status_code == 412:
                err_json = e.response.json()
                if "accountId-must-be-different" in err_json.get("errorCode", ""):
                    print("Already on this account. Skipping switch.")
                    return {
                        "cst": self.api_client.cst,
                        "x_security_token": self.api_client.x_security_token
                    }
            raise e

    def delete(self) -> bool:
        """
        Logs out (DELETE /session).
        """
        try:
            # We don't strictly need to raise on non-204 here if we just want to clear local state,
            # but strict API compliance implies checking success.
            self.api_client.request("DELETE", "/session", version="1")
        except Exception:
            # Even if the API call fails, we probably want to clear local tokens
            pass
            
        self.api_client.clear_tokens()
        self.account_id = None
        return True
