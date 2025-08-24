import asyncio
import websockets

async def chat():
    uri = "ws://127.0.0.1:8000/ws"  # server IP
    async with websockets.connect(uri) as websocket:
        async def sender():
            while True:
                msg = await asyncio.get_event_loop().run_in_executor(None, input, ">>> ")
                await websocket.send(msg)

        async def receiver():
            while True:
                try:
                    response = await websocket.recv()
                    print("<<", response)
                except websockets.ConnectionClosed:
                    break

        await asyncio.gather(sender(), receiver())

if __name__ == "__main__":
    asyncio.run(chat())
