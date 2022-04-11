from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatRoom
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
            new_room.save()
            return redirect("home")
    else:
        form = CreateRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form, 'error': error})


@login_required
def room(request, room_name):
    chats = []

    room = ChatRoom.objects.filter(name=room_name).first()
    if not room:
        return render(request, 'char/error.html')

    chats = Chat.objects.filter(room=room)

    characters=Character.objects.filter(room=room)

    if request.user!=room.gamemaster:
        playerCharacters = characters.filter(user=request.user)
        otherCharactersList = characters.exclude(user=request.user)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'chats': chats,
            'playerCharacters': playerCharacters,
            'otherCharactersList': otherCharactersList,
        })
    else:
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'chats': chats,
            'playerCharacters': characters,
        })
