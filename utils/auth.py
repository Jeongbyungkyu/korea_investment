import json
import requests
from datetime import datetime
from pathlib import Path

from config.settings import *

class TokenManager:
    def __init__(self):
        self.token = None
        self._load_token()

    def _load_token(self) -> None:
        """Load token from file if exists and valid"""
        try:
            if Path(TOKEN_FILE).exists():
                print("Found existing token file")
                with open(TOKEN_FILE, 'r') as f:
                    data = json.load(f)
                    self.token = data
                    print("Loaded token from file")
        except Exception as e:
            print(f"Error loading token: {e}")
            self.token = None

    def _save_token(self, token_data: dict) -> None:
        """Save token to file"""
        try:
            with open(TOKEN_FILE, 'w') as f:
                json.dump(token_data, f)
                print("Token saved to file")
        except Exception as e:
            print(f"Error saving token: {e}")

    def get_token(self) -> str:
        """Get approval key for websocket"""
        try:
            url = f"{BASE_URL}/oauth2/Approval"
            headers = {"content-type": "application/json"}
            body = {
                "grant_type": "client_credentials",
                "appkey": APP_KEY,
                "secretkey": APP_SECRET
            }
            
            print("Requesting new approval key...")
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            
            token_data = response.json()
            print("Got new approval key")
            
            approval_key = token_data["approval_key"]
            self._save_token(token_data)
            
            return approval_key
            
        except Exception as e:
            print(f"Error getting approval key: {e}")
            raise

token_manager = TokenManager()