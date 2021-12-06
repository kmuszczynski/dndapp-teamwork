from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CreateRequestAddToRoomForm
from charsheets.models import Character
from chat.models import CharacterBelongsToRoom, ChatRoom
from .models import UserToRoomRequest

# Create your views here.

@login_required
def request_add_user_to_room(request):
    if request.method=='POST':
        form = CreateRequestAddToRoomForm(request.POST)
        if form.is_valid():
            newRequest = form.save(commit=False)
            newRequest.save()
            return redirect('home')
    else:
        form = CreateRequestAddToRoomForm()
        form.fields['character'].queryset=Character.objects.filter(user=request.user)
    
    return render(request, 'request/add_user_to_room_request.html', {'form': form})

@login_required
def viewAllRequest(request):
    requests=UserToRoomRequest.objects.filter(room__gamemaster=request.user)
    if request.method == 'POST':
        getRequest = UserToRoomRequest.objects.get(pk=int(request.POST.get("request_id")))
        print(getRequest)
        if request.POST.get("status") == "accept":
            CharacterBelongsToRoom.objects.create(room=getRequest.room, character=getRequest.character)
        getRequest.delete()
    return render(request, 'request/all_request.html', {'requests': requests})

@login_required
def more_info_about_request_user_to_room(request, request_pk):
    getRequest=UserToRoomRequest.objects.get(pk=request_pk)
    if request.method == 'POST':
        if request.POST.get("status") == "accept":
            CharacterBelongsToRoom.objects.create(room=getRequest.room, character=getRequest.character)
        getRequest.delete()
        return redirect('viewallrequest')
    return render(request, 'request/more_about_request.html', {'request': getRequest})

#to będzie trzeba gdzieś przerzucić, ale wstępnie jest tutaj
@login_required
def view_all_gameroom(request):
    gm_room=ChatRoom.objects.filter(gamemaster=request.user)
    characters_room=CharacterBelongsToRoom.objects.filter(character__user=request.user)
    return render(request, 'request/all_room.html', {
        'gm_room': gm_room,
        'characters_room': characters_room,
    })