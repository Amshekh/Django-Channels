# In this i will send message to group outside the consumer from somewhere else like views.py. So goto code on views.py

from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Group
from channels.db import database_sync_to_async

class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        print('Websocket connected')
        print('Channel Layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)

        self.group_name = self.scope['url_route']['kwargs']['group__name']
        print('Group Name :', self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def receive_json(self, content, **kwargs):
        print('Message Received from client', content)

        group = Group.objects.get(name = self.group_name)
        chat = Chat(
            content = content['msg'],
            group = group
        )
        chat.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',
                'message' : content['msg']
            }
        )

    def chat_message(self, event):  # This is method created by me. As in above 'type' is 'chat.message', so i will make method as 'chat_message' (Django convention)
        print('Event :', event)
        
        self.send_json({
            'message': event['message']  # The message send from here will reach frontend in "ws.onmessage" of index.html
        })

    def disconnect(self, close_code):
        print('Websocket disconnected', close_code)

        print('Channel Layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('Websocket connected')
        print('Channel Layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)

        self.group_name = self.scope['url_route']['kwargs']['group__name']
        print('Group Name :', self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()                 # As usual every asynchronous method will require async before declaration & await infront of every statement

    async def receive_json(self, content, **kwargs):
        print('Message Received from client', content)

        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        chat = Chat(
            content = content['msg'],
            group = group
        )
        await database_sync_to_async(chat.save)()
                    
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message' : content['msg']
            }
        )

    async def chat_message(self, event):  # This is method created by me. As in above 'type' is 'chat.message', so i will make method as 'chat_message' (Django convention)
        print('Event :', event)
        
        await self.send_json({
            'message': event['message']  # The message send from here will reach frontend in "ws.onmessage" of index.html
        })

    async def disconnect(self, close_code):
        print('Websocket disconnected', close_code)
        print('Channel Layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )