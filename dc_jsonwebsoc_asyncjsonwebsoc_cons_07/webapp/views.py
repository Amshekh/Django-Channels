from django.shortcuts import render, HttpResponse
from .models import Chat, Group
from channels.layers import get_channel_layer   # i'm importing this to enable sending message from this view to group
from asgiref.sync import async_to_sync

def index(request, group_name):
    print("Group name : ", group_name)

    group = Group.objects.filter(name = group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group = group)
    else:
        group = Group(name = group_name)
        group.save()
    return render(request, 'webapp/index.html', {'groupname': group_name, 'chats':chats})

# Here i will send message to group from here (In earlier examples, i used to send it from consumers.py)

def msg_from_view(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'FullStack_WebDeveloper_Django',   # i have hard-coded group name
        {
            'type': 'chat.message',
            'message': 'Message from outside consumer (views)'
        }
    )
    return HttpResponse("Sending message from View to Consumer")
