from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatRoom, UserBelongsToRoom
from .forms import CreateRoomForm
from charsheets.models import Character


INVALID_CHARACTERS = " !\"#$%&'()*+,./:;<=>?@[\]^`{|}~"


@login_required
def create_chat_room(request):
    error = None
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if any(c in INVALID_CHARACTERS for c in form['name'].value()):
            error = "Wrong chat room name!"
        elif form.is_valid():
            new_room = form.save(commit=False)
            new_room.gamemaster = request.user
            new_room.status = 1 if form.cleaned_data['status'] == "PUBLIC" else 2
            new_room.grid_x = 0
            new_room.grid_y = 0
            new_room.save()
            return redirect("home")
    else:
        form = CreateRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form, 'error': error})


@login_required
def room(request, room_name):
    chats = []

    room = ChatRoom.objects.filter(name=room_name).first()
    gm = request.user == room.gamemaster
    user = UserBelongsToRoom.objects.filter(user=request.user).filter(room=room)
    if not room or (not user and not gm):
        return render(request, 'chat/error.html')

    chats = Chat.objects.filter(room=room)

    characters = Character.objects.filter(room=room)

    if not gm:
        playerCharacters = characters.filter(user=request.user)
        otherCharactersList = characters.exclude(user=request.user)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'gm': False,
            'chats': chats,
            'playerCharacters': playerCharacters,
            'otherCharactersList': otherCharactersList,
            'x': range(room.grid_x),
            'y': range(room.grid_y),
        })
    else:
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'gm': True,
            'chats': chats,
            'playerCharacters': characters,
            'x': range(room.grid_x),
            'y': range(room.grid_y),
        })
