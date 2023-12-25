import asyncio
import websockets
import json
import requests


async def server(websocket):
    try:
        print(f"Новое подключение: {websocket.remote_address}")
        while True:
            ticker = str(await websocket.recv()).upper()
            metadata = requests.get("https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/"
                                    "securities.json?iss.meta=off&iss.only=marketdata&marketdata.columns=LAST").json()
            value = []
            for i in range(0, len(metadata['marketdata']['data'])):
                value.append(metadata['marketdata']['data'][i][0])
            if ticker in shares:
                ind = shares.index(ticker)
                data = json.dumps(value[ind])
                await websocket.send(data)
            else: await websocket.send("404")
    except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError):
        print(f"Клиент {websocket.remote_address} отключился")


metadata = requests.get("https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/"
                        "securities.json?iss.meta=off&iss.only=marketdata&marketdata.columns=SECID").json()
shares = []
for i in range(0, len(metadata['marketdata']['data'])):
    shares.append(metadata['marketdata']['data'][i][0])

start_server = websockets.serve(server, "localhost", 1111)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
