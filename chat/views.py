from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatRoom
from charsheets.models import Character
from charsheets.forms import CharacterList, CharacterForm

@login_required
def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    character=None
    form=None
    room=ChatRoom.objects.filter(name=room_name).first()
    chats=[]

    characterListForm = CharacterList()
    characterListForm.fields['list'].queryset=Character.objects.filter(user=request.user)

    if request.method == 'POST':
        character=get_object_or_404(Character, pk=request.POST.get("list"))
        form=CharacterForm(instance=character)

    if room:
        chats=Chat.objects.filter(room=room)
    else:
        room=ChatRoom(name=room_name)
        room.save()

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chats': chats,
        'character': character,
        'characterListForm': characterListForm,
        'form': form
    })
