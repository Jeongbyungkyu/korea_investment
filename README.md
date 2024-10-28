# Korea Investment API Client

한국투자증권 Open API를 쉽게 사용할 수 있는 Python 클라이언트입니다.

## 기능

- OAuth 2.0 인증 지원
- 실전/모의 투자 환경 설정
- 환경 변수를 통한 설정 관리

## 시작하기

### 1. 설치 요구사항

```bash
pip install python-dotenv requests
```

### 2. 환경 설정

`.env` 파일을 생성하고 다음 정보를 입력하세요:

```
# 한국투자증권 API 설정
APP_KEY=your_app_key
APP_SECRET=your_app_secret
ACCOUNT_NUMBER=your_account_number
ACCOUNT_CODE=your_account_code

# 실전/모의 투자 설정
IS_PROD=False
```

### 3. 사용 예시

```python
from auth import KoreaInvestmentAuth

# 인증 객체 생성
auth = KoreaInvestmentAuth()

# Access Token 발급
token_info = auth.obtain_access_token()

# API 요청에 사용할 헤더 얻기
headers = auth.get_headers()
```

## 라이센스

MIT License

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request