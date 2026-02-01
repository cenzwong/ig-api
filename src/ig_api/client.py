import os
import requests
from dotenv import load_dotenv

class IGClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("IG_API_KEY")
        self.username = os.getenv("IG_USERNAME")
        self.password = os.getenv("IG_PASSWORD")
        self.env = os.getenv("IG_ENV", "demo")
        
        if self.env == "live":
            self.base_url = "https://api.ig.com/gateway/deal"
        else:
            self.base_url = "https://demo-api.ig.com/gateway/deal"
            
        self.cst = None
        self.x_security_token = None
        self.account_id = None

    def connect(self):
        print(f"Connecting to {self.env} environment...")
        
        url = f"{self.base_url}/session"
        
        headers = {
            "X-IG-API-KEY": self.api_key,
            "Version": "2",
            "Content-Type": "application/json",
            "Accept": "application/json; charset=UTF-8"
        }
        
        data = {
            "identifier": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Successful connection
            print("Connected Successfully!")
            
            # Extract tokens
            self.cst = response.headers.get("CST")
            self.x_security_token = response.headers.get("X-SECURITY-TOKEN")
            
            # Account info
            resp_json = response.json()
            self.account_id = resp_json.get("currentAccountId")
            
            return {
                "cst": self.cst,
                "x_security_token": self.x_security_token,
                "account_id": self.account_id
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Connection Failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                 print(f"Status Code: {e.response.status_code}")
                 print(f"Response Body: {e.response.text}")
            raise e
