import asyncio
import sys
from kis_client import KISClient
from kis_websocket import KISWebSocket


async def handle_data(data):
    """실시간 데이터 처리"""
    print(f"수신된 데이터: {data}")


async def main():
    # 모니터링 할 종목
    stock_code = "005930"  # 삼성전자

    # KIS 클라이언트 및 웹소켓 클라이언트 초기화
    client = KISClient()
    ws_client = KISWebSocket(client)

    # 프로그램 시작
    print("실시간 주식 데이터 수신을 시작합니다...")
    print(f"모니터링 종목: {stock_code}")

    try:
        # 웹소켓 연결
        if await ws_client.connect():
            # 종목 구독
            if await ws_client.subscribe(stock_code):
                print(f"{stock_code} 종목 구독 완료")
                # 실시간 데이터 수신 시작
                await ws_client.start_streaming(handle_data)
            else:
                print(f"{stock_code} 종목 구독 실패")
        else:
            print("웹소켓 연결 실패")
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        if ws_client:
            await ws_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")
        sys.exit(0)
