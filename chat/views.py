from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatRoom
from .forms import CreateRoomForm
from charsheets.models import Character


@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            newRoom = form.save(commit=False)
            newRoom.gamemaster = request.user
            newRoom.status = 1 if form.cleaned_data['status'] == "PUBLIC" else 2
            newRoom.save()
            return redirect("home")
    else:
        form = CreateRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form})


@login_required
def room(request, room_name):
    chats = []

    room = ChatRoom.objects.filter(name=room_name).first()
    
    if not room:
        return render(request, 'char/error.html')

    chats = Chat.objects.filter(room=room)
    gm = request.user == room.gamemaster
    characterList = Character.objects.filter(room=room)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chats': chats,
        'gm': gm,
        'characterList': characterList,
    })
