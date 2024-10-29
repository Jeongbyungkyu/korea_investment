import json
import websockets
import asyncio
from typing import Optional, Callable, Dict
from config.settings import *
from utils.auth import token_manager

class WebSocketClient:
    def __init__(self):
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False
        self.token = None

    async def connect(self) -> None:
        """Connect to websocket server"""
        try:
            self.token = token_manager.get_token()
            self.websocket = await websockets.connect(SOCKET_URL, ping_interval=None)
            self.running = True
            print("WebSocket connection established")
            await self._start_ping()
            await self._subscribe_stocks()
        except Exception as e:
            print(f"Connection error: {e}")
            self.running = False
            raise

    async def _start_ping(self):
        """Start ping/pong task"""
        async def ping_handler():
            while self.running:
                try:
                    print(".", end="", flush=True)
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Ping error: {e}")
                    break
        asyncio.create_task(ping_handler())

    async def _subscribe_stocks(self):
        """Subscribe to test stocks"""
        test_stocks = ['005930', '000660', '035720']  # 삼성전자, SK하이닉스, 카카오
        
        for stock_code in test_stocks:
            subscribe_data = {
                "header": {
                    "approval_key": self.token,
                    "custtype": "P",
                    "tr_type": "1",
                    "content-type": "utf-8"
                },
                "body": {
                    "input": {
                        "tr_id": "H0STCNT0",
                        "tr_key": stock_code
                    }
                }
            }
            
            try:
                print(f"\nSubscribing to {stock_code}...")
                await self.websocket.send(json.dumps(subscribe_data))
                response = await self.websocket.recv()
                print(f"Subscription response: {response}")
            except Exception as e:
                print(f"Error subscribing to {stock_code}: {e}")

            await asyncio.sleep(0.5)  # Prevent too many requests at once

    async def run(self):
        """Main run loop"""
        while self.running:
            try:
                message = await self.websocket.recv()
                if message[0] in ('0', '1'):  # Real-time data
                    print(f"\nReceived data: {message}")
                else:
                    data = json.loads(message)
                    if data['header']['tr_id'] != 'PINGPONG':
                        print(f"\nReceived message: {data}")
            except websockets.ConnectionClosed:
                print("\nConnection closed")
                break
            except Exception as e:
                print(f"\nError in message loop: {e}")
                continue

    async def disconnect(self):
        """Disconnect from websocket server"""
        self.running = False
        if self.websocket:
            await self.websocket.close()
            print("\nWebSocket disconnected")

# Global instance
ws_client = WebSocketClient()