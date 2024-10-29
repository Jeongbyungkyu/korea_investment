korea_investment/
├── .env # 환경 설정 파일
├── token.json # 토큰 저장용 파일 (자동 생성)
├── main.py # 메인 실행 파일
│
├── config/
│ ├── **init**.py
│ └── settings.py # 설정값 로드
│
├── models/
│ ├── **init**.py
│ └── token.py # 토큰 데이터 모델
│
├── utils/
│ ├── **init**.py
│ ├── auth.py # 토큰 관리 클래스
│ └── api_client.py # 웹소켓 클라이언트
│
├── analysis/
│ ├── **init**.py
│ └── technical.py # 기술적 분석 클래스 (StockAnalyzer)
│
└── strategy/
├── **init**.py
└── stock_selector.py # 종목 선정 클래스 (TopStockSelector)

현재 구현된 주요 기능:

1. config/: 환경 설정 관리
2. models/: 토큰 데이터 구조
3. utils/: 웹소켓 연결 및 인증
4. analysis/: 종목 분석 로직
5. strategy/: 종목 선정 로직

///////2024.10.29

### 1. 현재까지 구현된 기능

A. 기본 인프라

- 환경 설정 (.env) 기반 설정 관리
- 웹소켓 연결 및 토큰 관리
- 모의투자/실전투자 분기 처리

B. 웹소켓 클라이언트 (utils/api_client.py)

- 자동 재연결
- 실시간 데이터 구독
- PINGPONG 처리
- 에러 핸들링

C. 토큰 관리 (utils/auth.py, models/token.py)

- 토큰 로컬 저장/로드
- 4시간 만료 체크
- 자동 갱신

D. 분석 로직 (analysis/technical.py)

- 추세 분석 (이동평균선)
- 거래량 분석
- 외국인/기관 수급 분석
- 박스권 돌파 분석
- 캔들패턴 분석

E. 종목 선정 전략 (strategy/stock_selector.py)

- 종합 점수 계산
- TOP 10 종목 선정 로직

### 2. 테스트 완료된 부분

- 웹소켓 연결
- 토큰 관리
- 실시간 데이터 구독 설정

### 3. 다음 구현 필요 사항

A. 데이터 수집/저장

- 실시간 데이터를 DB나 파일로 저장
- 일봉/분봉 데이터 수집
- 외국인/기관 수급 데이터 수집

B. 분석 기능 연동

- 실시간 데이터와 분석 로직 연결
- 정기적인 분석 수행
- 결과 저장 및 업데이트

C. 알림/모니터링

- 조건 충족시 알림
- 성능 모니터링
- 에러 로깅

### 4. 코드 수정 필요 사항

- analysis/technical.py의 실제 데이터 연동 테스트
- TopStockSelector의 실시간 처리 최적화
- 메모리 관리 및 성능 최적화

### 5. 테스트 필요 사항

- 장 시간 중 실시간 데이터 수신 테스트
- 분석 로직 정확도 검증
- 메모리 누수 체크
- 장시간 운영 안정성 테스트

### 6. 다음 작업 시작점

```python
# main.py에 데이터 저장 로직 추가 필요
async def save_market_data(message):
    # 데이터 파싱 및 저장
    pass

# analysis/technical.py와 실제 데이터 연동
async def run_analysis():
    # 저장된 데이터 로드 및 분석
    pass

# 다음 실행시 시작 지점
if __name__ == "__main__":
    initialize_database()  # 추가 필요
    start_data_collection()  # 추가 필요
    run_analysis_scheduler()  # 추가 필요
```
