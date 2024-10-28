import os
import json
import requests
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class KoreaInvestmentAuth:
    def __init__(self):
        self.app_key = os.getenv('APP_KEY')
        self.app_secret = os.getenv('APP_SECRET')
        self.account_number = os.getenv('ACCOUNT_NUMBER')
        self.account_code = os.getenv('ACCOUNT_CODE')
        self.is_prod = os.getenv('IS_PROD', 'False').lower() == 'true'
        
        # 실전/모의 투자 환경에 따른 도메인 설정
        self.domain = "https://openapi.koreainvestment.com:9443" if self.is_prod else "https://openapivts.koreainvestment.com:29443"
        
        # 토큰 저장 변수
        self.access_token = None
        self.token_type = None
        self.expires_in = None
    
    def obtain_access_token(self):
        """Access Token 발급"""
        url = f"{self.domain}/oauth2/tokenP"
        
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data.get('access_token')
            self.token_type = token_data.get('token_type')
            self.expires_in = token_data.get('expires_in')
            
            return {
                'access_token': self.access_token,
                'token_type': self.token_type,
                'expires_in': self.expires_in
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            return None

    def get_headers(self):
        """API 요청에 사용할 헤더 반환"""
        if not self.access_token:
            raise ValueError("Access token is not available. Call obtain_access_token() first.")
            
        return {
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "CTSC0001R",  # TR ID는 API별로 다름
            "custtype": "P",  # 개인
        }

# 사용 예시
if __name__ == "__main__":
    auth = KoreaInvestmentAuth()
    token_info = auth.obtain_access_token()
    
    if token_info:
        print("Access Token 발급 성공:")
        print(json.dumps(token_info, indent=2))
        
        print("\n인증 헤더:")
        print(json.dumps(auth.get_headers(), indent=2))
    else:
        print("Access Token 발급 실패")