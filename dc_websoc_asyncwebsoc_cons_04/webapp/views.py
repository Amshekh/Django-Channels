from django.shortcuts import render
from .models import Chat, Group

def index(request, group_name):
    print('Group Name : ', group_name)
    group = Group.objects.filter(name = group_name).first()
    chats = []
    if group:   
        chats = Chat.objects.filter(group = group)
    else:
        group = Group(name = group_name)
        group.save()
    return render(request, 'webapp/index.html', 
    {'groupname':group_name, 'chats':chats})
