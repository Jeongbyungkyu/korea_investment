import os
import json
import asyncio
import websockets
from dotenv import load_dotenv


class KISWebSocket:
    def __init__(self, client):
        """
        Args:
            client: KISClient 인스턴스 (토큰 관리용)
        """
        self.client = client
        self.is_prod = os.getenv("IS_PROD", "False").lower() == "true"
        self.ws_url = (
            "ws://ops.koreainvestment.com:21000"
            if self.is_prod
            else "ws://ops.koreainvestment.com:31000"
        )
        self.ws = None
        self.running = False
        self.subscribed_symbols = set()

    async def connect(self):
        """웹소켓 연결 수립"""
        try:
            approval_key = await self.client.get_approval_key()
            if not approval_key:
                print("Approval key 발급 실패")
                return False

            self.ws = await websockets.connect(
                self.ws_url,
                extra_headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "Connection": "Upgrade",
                    "Upgrade": "websocket",
                },
            )

            print("웹소켓 연결 성공")
            self.running = True
            return True

        except Exception as e:
            print(f"웹소켓 연결 실패: {str(e)}")
            self.running = False
            return False

    async def subscribe(self, symbol, tr_id="H0STASP0"):
        """특정 종목 구독"""
        if not self.ws:
            print("웹소켓이 연결되어 있지 않습니다.")
            return False

        if symbol in self.subscribed_symbols:
            print(f"{symbol} 종목은 이미 구독 중입니다.")
            return True

        try:
            subscribe_data = {
                "header": {
                    "approval_key": await self.client.get_approval_key(),
                    "custtype": "P",
                    "tr_type": "1",
                    "content-type": "utf-8",
                },
                "body": {"input": {"tr_id": tr_id, "tr_key": symbol}},
            }

            await self.ws.send(json.dumps(subscribe_data))
            response = await self.ws.recv()
            response_data = json.loads(response)

            # ALREADY IN SUBSCRIBE도 성공으로 처리
            if response_data.get("body", {}).get("msg1") in [
                "SUBSCRIBE SUCCESS",
                "ALREADY IN SUBSCRIBE",
            ]:
                self.subscribed_symbols.add(symbol)
                print(f"{symbol} 종목 구독 성공")
                return True
            else:
                print(f"종목 구독 실패 ({symbol}): {response}")
                return False

        except Exception as e:
            print(f"구독 실패 ({symbol}): {str(e)}")
            return False

    async def start_streaming(self, callback):
        """실시간 데이터 수신"""
        while self.running:
            try:
                if not self.ws:
                    break

                data = await self.ws.recv()
                # 데이터가 문자열인 경우 JSON으로 파싱 시도
                try:
                    parsed_data = json.loads(data)
                    await callback(parsed_data)
                except json.JSONDecodeError:
                    # JSON 파싱 실패 시 원본 데이터 처리
                    await self.handle_realtime_data(data)

            except websockets.exceptions.ConnectionClosed:
                print("웹소켓 연결이 종료되었습니다.")
                break

            except Exception as e:
                print(f"데이터 수신 중 오류: {str(e)}")
                break

        self.running = False
        print("스트리밍이 종료되었습니다.")

    async def handle_realtime_data(self, data):
        """실시간 데이터 처리"""
        try:
            # 데이터가 | 로 구분되는 경우 처리
            if isinstance(data, str) and "|" in data:
                fields = data.split("|")
                if len(fields) >= 4:  # 최소 필드 수 확인
                    encrypt_yn = fields[0]  # 암호화 여부
                    tr_id = fields[1]  # TR ID
                    data_cnt = fields[2]  # 데이터 건수
                    recv_data = fields[3]  # 실제 데이터

                    # 실시간 데이터 파싱 (^ 구분자 사용)
                    if "^" in recv_data:
                        values = recv_data.split("^")
                        print(f"실시간 데이터 수신: {values}")
            else:
                print(f"기타 메시지: {data}")

        except Exception as e:
            print(f"데이터 처리 중 오류: {str(e)}")

    async def close(self):
        """웹소켓 연결 종료"""
        self.running = False
        if self.ws:
            try:
                for symbol in list(self.subscribed_symbols):
                    unsubscribe_data = {
                        "header": {
                            "approval_key": await self.client.get_approval_key(),
                            "custtype": "P",
                            "tr_type": "2",
                            "content-type": "utf-8",
                        },
                        "body": {"input": {"tr_id": "H0STASP0", "tr_key": symbol}},
                    }
                    await self.ws.send(json.dumps(unsubscribe_data))
                    print(f"{symbol} 종목 구독 해제")

                await self.ws.close()
                self.ws = None
                print("웹소켓 연결이 종료되었습니다.")
            except Exception as e:
                print(f"연결 종료 중 오류: {str(e)}")
