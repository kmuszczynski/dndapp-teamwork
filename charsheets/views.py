from charsheets.forms import CharacterForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Character
from chat.models import ChatRoom
from django.contrib.auth.decorators import login_required


# tworzenie postaci z forma opartego na modelu
@login_required
def create_character(request, room_name):

    room = ChatRoom.objects.filter(name=room_name).first()
    if not room:
        return render(request, 'char/error.html')

    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            newCharacter = form.save(commit=False)
            newCharacter.user = request.user
            newCharacter.room = room
            newCharacter.save()
            return redirect("room", room_name=room.name)
    else:
        form = CharacterForm()
    return render(request, 'charsheets/createchar.html', {'form': form})


@login_required
def view_character(request, character_pk):
    character = get_object_or_404(Character, pk=character_pk, user=request.user)
    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect("room", room_name=character.room)
    else:
        form = CharacterForm(instance=character)
    return render(request, 'charsheets/viewcharacter.html', {'character':character, 'form':form})
