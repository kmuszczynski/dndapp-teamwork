from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CreateRequestAddToRoomForm
from charsheets.models import Character
from chat.models import CharacterBelongsToRoom, ChatRoom
from .models import UserToRoomRequest
from .fun import create_CharacterBelongsToRoom

# Create your views here.

@login_required
def request_add_user_to_room(request):
    error=None
    if request.method=='POST':
        form = CreateRequestAddToRoomForm(request.POST)
        if form.is_valid():
            room_check=form.cleaned_data.get("room")
            character=CharacterBelongsToRoom.objects.filter(room=form.cleaned_data.get("room")).filter(character=form.cleaned_data.get("character"))
            if len(character)==0:
                if room_check.gamemaster!=request.user:
                    newRequest = form.save(commit=False)
                    newRequest.save()
                    return redirect('home')
                else:
                    error="You are GM in this room!!!"
            else:
                error="Character already belongs to this room!!!"
    else:
        form = CreateRequestAddToRoomForm()

    form.fields['character'].queryset=Character.objects.filter(user=request.user)
    return render(request, 'request/add_user_to_room_request.html', {'form': form, 'error': error})

@login_required
def viewAllRequest(request):
    requests=UserToRoomRequest.objects.filter(room__gamemaster=request.user)
    if request.method == 'POST':
        getRequest = UserToRoomRequest.objects.get(pk=int(request.POST.get("request_id")))
        if request.POST.get("status") == "accept":
            create_CharacterBelongsToRoom(getRequest)
        getRequest.delete()
    return render(request, 'request/all_request.html', {'requests': requests})

@login_required
def more_info_about_request_user_to_room(request, request_pk):
    getRequest=UserToRoomRequest.objects.get(pk=request_pk)
    if request.method == 'POST':
        if request.POST.get("status") == "accept":
            create_CharacterBelongsToRoom(getRequest)
        getRequest.delete()
        return redirect('viewallrequest')
    return render(request, 'request/more_about_request.html', {'request': getRequest})

#to będzie trzeba gdzieś przerzucić, ale wstępnie jest tutaj
@login_required
def view_all_gameroom(request):
    gm_room=ChatRoom.objects.filter(gamemaster=request.user)
    characters_room=CharacterBelongsToRoom.objects.filter(character__user=request.user)
    if request.method=='POST':
        character_old=CharacterBelongsToRoom.objects.filter(room__name=request.POST.get("room")).filter(character__user=request.user).get(status=1)
        character_old.status=2
        character_old.save()
        character_new=CharacterBelongsToRoom.objects.filter(room__name=request.POST.get("room")).get(character__name=request.POST.get("character"))
        character_new.status=1
        character_new.save()
        return redirect('room', room_name=request.POST.get("room"))
    return render(request, 'request/all_room.html', {
        'gm_room': gm_room,
        'characters_room': characters_room,
    })