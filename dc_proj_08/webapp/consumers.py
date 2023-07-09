from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Group
from channels.db import database_sync_to_async
import json

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('WebSocket Connected', event)
        print('Channel Layer', self.channel_layer)
        print('Channel Name', self.channel_name)
        
        self.group_name = self.scope['url_route']['kwargs']['group__name']

        print('Group Name : ', self.group_name)

        # adding channel to either a new group or existing group. Here we have made group name dynamic.
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, 
            self.channel_name       # self.channel_layer.group_add is asynchronous function & needs to be converted to synchronous
            )

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message Received from Client is : ', event['text'])
        print('The type of Message Received from Client is : ', type(event['text']))
        data = json.loads(event['text'])
        print('Chat Message', data['msg'])

        group = Group.objects.get(name = self.group_name)

        if self.scope['user'].is_authenticated:  # if user is authenticated then save chat, otherwise goto else part 
            chat = Chat(
                content = data['msg'],
                group = group
            )
            chat.save()  # if someone new joins an existing group, he/she will be able to see previous chat

            data['user'] = self.scope['user'].username
            print('Complete data', data)
            print('Type of Complete data', type(data))

            async_to_sync (self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': json.dumps(data) # we are using dumps method as we want to convet python dictionary to jason string, so it can be displayed in browser
                }
            )
        else:    
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "To continue chat, kindly login", "user" : "guest_user"}) # As user is not logged in else case, he/she will be guest_user
            })
        
    def chat_message(self, event):  # creating a method manually 
        print('Original message is:', event['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })


    def websocket_disconnect(self, event):
        print('WebSocket Disconnected', event)
        print('Channel Layer', self.channel_layer)
        print('Channel Name', self.channel_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name       # self.channel_layer.group_add is asynchronous function & needs to be converted to synchronous
            )
        self.send({
            'type': 'websocket.stop'
        })

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('WebSocket Connected', event)
        print('Channel Layer', self.channel_layer)
        print('Channel Name', self.channel_name)

        self.group_name = self.scope['url_route']['kwargs']['group__name']

        print('Group Name : ', self.group_name)

        # adding channel to either a new group or existing group. Here FullStack Developer is group name.
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name       # In case of asynchronous, we don't need any conversion as it's already asynchronous
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message Received from Client is : ', event['text'])
        print('The type of Message Received from Client is : ', type(event['text']))

        data = json.loads(event['text'])
        print('Chat Message', data['msg'])

        print(self.scope['user'])

        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)

        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            await database_sync_to_async(chat.save)()

            data['user'] = self.scope['user'].username
            print('Complete data', data)
            print('Type of Complete data', type(data))

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': json.dumps(data)
                }
            )
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "To continue chat, kindly login", "user" : "guest_user"})
            })
        
    async def chat_message(self, event):  # creating a method manually 
        print('Original message is:', event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })


    async def websocket_disconnect(self, event):
        print('WebSocket Disconnected', event)
        print('Channel Layer', self.channel_layer)
        print('Channel Name', self.channel_name)
        
        self.channel_layer.group_add(
            self.group_name, self.channel_name       # self.channel_layer.group_add is asynchronous function & needs to be converted to synchronous
            )
        await self.send({
            'type': 'websocket.stop'
        })