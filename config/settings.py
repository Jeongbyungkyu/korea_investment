import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
ACCOUNT_NUMBER = os.getenv('ACCOUNT_NUMBER')
ACCOUNT_CODE = os.getenv('ACCOUNT_CODE')

# Environment Configuration
IS_PROD = os.getenv('IS_PROD', 'False').lower() == 'true'
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# WebSocket URLs
SOCKET_URL = 'ws://ops.koreainvestment.com:21000' if IS_PROD else 'ws://ops.koreainvestment.com:31000'

# REST API URLs
BASE_URL = 'https://openapi.koreainvestment.com:9443' if IS_PROD else 'https://openapivts.koreainvestment.com:29443'

# Token file path
TOKEN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token.json')