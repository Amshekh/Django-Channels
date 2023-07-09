from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from time import sleep
import asyncio

class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print('WebSocket Connected')
        self.accept()   # accept connection so that websocket properly remains connected

    def receive(self, text_data=None, bytes_data=None):
        print('Message Received from Client', text_data)
        for i in range(1, 11):
            self.send(text_data=str(i))  # i'm sending data to client (Postman in this case)
            sleep(2)

    def disconnect(self, close_code):
        print('WebSocket Disconnected', close_code)


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('WebSocket Connected')
        await self.accept()   # accept connection so that websocket properly remains connected

    async def receive(self, text_data=None, bytes_data=None):
        print('Message Received from Client', text_data)
        for i in range(1, 11):
            await self.send(text_data=str(i))  # i'm sending data to client (Postman in this case)
            await asyncio.sleep(2)


    async def disconnect(self, close_code):
        print('WebSocket Disconnected', close_code)