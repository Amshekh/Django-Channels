from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Group
from channels.db import database_sync_to_async
import json

class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('WebSocket Connected')
        print('Channel Layer : ', self.channel_layer)
        print('Channel Name : ', self.channel_name)

        self.group_name = self.scope['url_route']['kwargs']['group__name']

        print("Groupname : ", self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, 
            self.channel_name       # self.channel_layer.group_add is asynchronous function & needs to be converted to synchronous
        )

        self.accept()   # accept connection so that websocket properly remains connected

    def receive(self, text_data=None, bytes_data=None):
        print('Message Received from Client', text_data)

        data = json.loads(text_data)
        print('Data : ', data)
        message = data['msg']

        group = Group.objects.get(name = self.group_name)

        if self.scope['user'].is_authenticated:  # if user is authenticated then save chat, otherwise goto else part 
            chat = Chat(
                content = data['msg'],
                group = group
            )
            chat.save()  # if someone new joins an existing group, he/she will be able to see previous chat

            async_to_sync (self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:    
            self.send(text_data=json.dumps({
                "msg": "To continue chat, kindly login" # As user is not logged in else case, he/she will be guest_user
            }))

    def chat_message(self, event):
        self.send(text_data= json.dumps({
            'msg': event['message']
        }))

    def disconnect(self, close_code):
        print('WebSocket Disconnected', close_code)
        print('Channel Layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('WebSocket Connected')
        print('Channel Layer : ', self.channel_layer)
        print('Channel Name : ', self.channel_name)

        self.group_name = self.scope['url_route']['kwargs']['group__name']

        print("Groupname : ", self.group_name)

        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name       # self.channel_layer.group_add is asynchronous function & needs to be converted to synchronous
        )
        await self.accept()   # accept connection so that websocket properly remains connected

    async def receive(self, text_data=None, bytes_data=None):
        print('Message Received from Client', text_data)
        
        data = json.loads(text_data)
        print('Data : ', data)

        message = data['msg']

        group = await database_sync_to_async(Group.objects.get)(name= self.group_name)

        if self.scope['user'].is_authenticated:
            chat = Chat(
            content = data['msg'],
            group = group
            )
        
            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            await self.send(text_data=json.dumps({
                "msg": "To continue chat, kindly login" # As user is not logged in else case, he/she will be guest_user
            }))

    async def chat_message(self, event):
        await self.send(text_data= json.dumps({
            'msg': event['message']
        }))
        

    async def disconnect(self, close_code):
        print('WebSocket Disconnected', close_code)
        print('Channel Layer :', self.channel_layer)
        print('Channel Name :', self.channel_name)

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )