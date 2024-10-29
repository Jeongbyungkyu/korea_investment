import asyncio
from utils.api_client import ws_client

async def main():
    try:
        print("Starting WebSocket connection...")
        await ws_client.connect()
        print("Starting main loop...")
        await ws_client.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        await ws_client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")