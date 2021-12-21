from asyncio.windows_events import NULL
import re
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import CharacterBelongsToRoom, Chat, ChatRoom
from .forms import CreateRoomForm

@login_required
def create_chat_room(request):
    if request.method=='POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            newRoom = form.save(commit=False)
            newRoom.gamemaster = request.user
            newRoom.save()
            return redirect("home")
    else:
        form = CreateRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form})

@login_required
def room(request, room_name):
    chats=[]

    #sprawdzanie czy istnieje pokój
    room=ChatRoom.objects.filter(name=room_name).first()
    if room:
        chats=Chat.objects.filter(room=room)
    else:
        return render(request, 'chat/error.html')

    #sprawdzanie czy gracz jest gm
    if(request.user==room.gamemaster):
        characterList=CharacterBelongsToRoom.objects.filter(room__name=room_name)
        print(characterList)
        return render(request, 'chat/room_gm.html', {
            'room_name': room_name,
            'chats': chats,
            'characterList': characterList,
        })
    
    #sprawdzanie czy gracz ma bohatera
    characterinroom=CharacterBelongsToRoom.objects.filter(character__user=request.user, room__name=room_name)
    
    if characterinroom:
        return render(request, 'chat/room_player.html', {
            'room_name': room_name,
            'chats': chats,
            'character': characterinroom.get(status=1),
        })
    else:
        return render(request, 'chat/error.html')
