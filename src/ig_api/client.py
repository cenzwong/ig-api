import os
from dotenv import load_dotenv
from .core.api import ApiClient
from .services.session import SessionService

class IGClient:
    """
    Client facade for the IG Trading API.
    
    Attributes:
        session (SessionService): Service for session management.
    """

    def __init__(self):
        """
        Initializes the IGClient.
        Loads environment variables and sets up the core API client and services.
        """
        load_dotenv()
        self.api_key = os.getenv("IG_API_KEY")
        self.username = os.getenv("IG_USERNAME")
        self.password = os.getenv("IG_PASSWORD")
        self.env = os.getenv("IG_ENV", "demo")
        
        if self.env == "live":
            self.base_url = "https://api.ig.com/gateway/deal"
        else:
            self.base_url = "https://demo-api.ig.com/gateway/deal"
            
        # Core
        self.api_client = ApiClient(self.base_url, self.api_key)
        
        # Services
        self.session = SessionService(self.api_client)

    def connect(self) -> dict:
        """
        Convenience method to authenticates and establish a session.
        Delegates to self.session.create().
        """
        return self.session.create(self.username, self.password)

    def logout(self) -> bool:
        """
        Convenience method to logout.
        Delegates to self.session.delete().
        """
        return self.session.delete()