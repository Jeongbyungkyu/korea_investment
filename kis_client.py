import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv


class KISClient:
    def __init__(self):
        load_dotenv()
        self.app_key = os.getenv("APP_KEY")
        self.app_secret = os.getenv("APP_SECRET")
        self.is_prod = os.getenv("IS_PROD", "False").lower() == "true"

        # 실전/모의 도메인 설정
        self.base_url = (
            "https://openapi.koreainvestment.com:9443"
            if self.is_prod
            else "https://openapivts.koreainvestment.com:29443"
        )

        # 토큰 캐시 파일 경로
        self.token_cache_file = "token_cache.json"

    def load_cached_token(self):
        """저장된 토큰 정보 로드"""
        try:
            if os.path.exists(self.token_cache_file):
                with open(self.token_cache_file, "r") as f:
                    cache_data = json.load(f)

                # 만료 시간 확인
                expires_at = datetime.strptime(
                    cache_data["expires_at"], "%Y-%m-%d %H:%M:%S"
                )
                if datetime.now() < expires_at:
                    print("캐시된 토큰을 사용합니다.")
                    return cache_data
        except Exception as e:
            print(f"캐시 파일 로드 중 오류: {str(e)}")
        return None

    def save_token_cache(self, token_data):
        """토큰 정보 캐시 파일로 저장"""
        try:
            with open(self.token_cache_file, "w") as f:
                json.dump(token_data, f, indent=2)
            print("토큰이 캐시 파일에 저장되었습니다.")
        except Exception as e:
            print(f"캐시 파일 저장 중 오류: {str(e)}")

    def get_access_token(self):
        """Access Token 발급 또는 캐시에서 로드"""
        cached_token = self.load_cached_token()
        if cached_token:
            return cached_token["access_token"]

        url = f"{self.base_url}/oauth2/tokenP"
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
        }
        headers = {"content-type": "application/json; charset=UTF-8"}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = response.json()

            token_info = {
                "access_token": response_data["access_token"],
                "token_type": response_data["token_type"],
                "expires_at": response_data["access_token_token_expired"],
            }

            self.save_token_cache(token_info)
            print("새로운 토큰이 발급되었습니다.")
            return token_info["access_token"]

        except Exception as e:
            print(f"토큰 발급 중 오류: {str(e)}")
            return None

    async def get_approval_key(self):
        """WebSocket용 approval key 발급"""
        url = f"{self.base_url}/oauth2/Approval"
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret,
        }
        headers = {"content-type": "application/json; charset=UTF-8"}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = response.json()
            approval_key = response_data.get("approval_key")
            return approval_key
        except Exception as e:
            print(f"Approval key 발급 중 오류: {str(e)}")
            return None


if __name__ == "__main__":
    client = KISClient()
    access_token = client.get_access_token()
    if access_token:
        print(f"Access Token: {access_token}")
