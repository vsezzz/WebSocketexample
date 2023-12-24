import asyncio
import websockets


async def client():
    uri = "ws://localhost:1111"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                ticker = input("Введите тикер (или 'exit' для выхода): ").upper()
                if ticker.lower() == 'exit':
                    print("Отключение от сервера...")
                    break
                await websocket.send(ticker)
                answer = await websocket.recv()
                if answer == "404":
                    print(f"Невозможно вывести цену тикера {ticker}")
                else:
                    print(f"Цена одного лота {ticker} на данный момент равна {answer}")
    except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError):
        print("Вас отключило от сервера")
    except ConnectionRefusedError:
        print("Невозможно подключиться к серверу")
    finally:
        print("Работа клиента завершена")

sergio = client()
asyncio.run(sergio)
