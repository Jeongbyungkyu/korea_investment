프로젝트 구조 및 설명:

파일 구조

Copykorea_investment/
├── .env                 # 환경변수 설정 파일
├── kis_client.py       # 토큰 관리 클라이언트
├── kis_websocket.py    # 웹소켓 연결 및 실시간 데이터 처리
├── main.py            # 메인 실행 파일
└── token_cache.json   # 토큰 캐시 파일 (자동 생성)

주요 컴포넌트 역할

a) kis_client.py:

토큰 관리 및 인증 처리
access_token과 approval_key 발급
토큰 캐싱 및 재사용

b) kis_websocket.py:

웹소켓 연결 관리
실시간 데이터 구독
데이터 스트리밍 처리

c) main.py:

프로그램 실행 진입점
단일 종목 모니터링 설정
데이터 처리 콜백 구현


설정 파일

a) .env 파일 구성:
CopyAPP_KEY=your_app_key
APP_SECRET=your_app_secret
IS_PROD=False
ACCOUNT_NUMBER=your_account
ACCOUNT_CODE=01

현재 구현된 기능:


REST API 토큰 인증
WebSocket 연결 및 인증
실시간 주식 호가 데이터 구독
자동 재연결 처리
에러 처리


사용된 API:


웹소켓 접속키 발급 (/oauth2/Approval)
실시간 주식호가 (H0STASP0)


실행 방법:

bashCopy# 1. 필요 패키지 설치
pip install websockets python-dotenv requests

# 2. 실행
python main.py

다음 구현 예정 사항:


실시간 데이터 파싱 및 처리
매매 로직 구현
거래량 분석
차트 데이터 처리
자동 매매 기능

주의사항:

.env 파일의 중요 정보 보호
실전/모의투자 환경 구분 주의
토큰 만료 시간 관리

다음 단계에서는:

실시간 데이터 파싱 및 저장
매매 전략 구현
거래량 분석 로직
을 구현할 예정입니다.

이어서 진행하실 때 어떤 부분부터 구현하기를 원하시는지 말씀해 주시면 됩니다.