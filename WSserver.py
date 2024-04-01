import asyncio
import websockets
import json
import requests


async def server(websocket):
    try:
        print(f"Новое подключение: {websocket.remote_address}")
        while True:
            ticker = str(await websocket.recv()).upper()
            metadata = requests.get(F"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{ticker}/"
                                    "securities.json?iss.meta=off&iss.only=marketdata&marketdata.columns=LAST").json()
            if metadata['marketdata']['data'] == []:
                await websocket.send("404")
            else:
                value = metadata['marketdata']['data'][0][0]
                data = json.dumps(value)
                await websocket.send(data)
    except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError):
        print(f"Клиент {websocket.remote_address} отключился")

start_server = websockets.serve(server, "localhost", 1111)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
