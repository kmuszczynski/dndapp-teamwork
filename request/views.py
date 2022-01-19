from tracemalloc import start
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
def request_add_user_to_room(request, room_name):
    error=None
    if request.method=='POST':
        form = CreateRequestAddToRoomForm(request.POST)
        if form.is_valid():
            character=CharacterBelongsToRoom.objects.filter(room__name=room_name).filter(character=form.cleaned_data.get("character"))
            character_request=UserToRoomRequest.objects.filter(room__name=room_name).filter(character=form.cleaned_data.get("character"))
            room = ChatRoom.objects.get(name=room_name)
            if len(character)==0 and len(character_request)==0:
                newRequest = form.save(commit=False)
                newRequest.room = room
                newRequest.save()
                return redirect('home')
            else:
                error="Character already belongs to this room!!!"
    else:
        form = CreateRequestAddToRoomForm()

    form.fields['character'].queryset=Character.objects.filter(user=request.user)
    return render(request, 'request/add_user_to_room_request.html', {'form': form, 'room':room_name, 'error': error})

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

@login_required
def all_public_room(request, id_side):
    next=False
    first=False
    error=None

    if request.method=='POST':
        if request.POST.get('id_new_side'):
            return redirect('allPublicRooms', id_side=request.POST.get('id_new_side'))
        if request.POST.get('search'):
            room_search_name=request.POST.get('search')
            try:
                room = ChatRoom.objects.get(name=room_search_name)
                if room.gamemaster == request.user:
                    error="You are gamemaster in this room"
                return redirect('addrequest', room_name=room)
            except ChatRoom.DoesNotExist:
                error="There is no room with that name"
        if request.POST.get('room'):
            room = ChatRoom.objects.get(name=request.POST.get('room'))
            return redirect('addrequest', room_name=room)
        else:
            return render(request, 'chat/error.html')

    ROOMS_ON_SIDE = 5
    allPublic = list(ChatRoom.objects.filter(status=1).exclude(gamemaster=request.user))
    allPublic_size = len(allPublic)
    start_index=ROOMS_ON_SIDE*id_side

    max_side_id = int(allPublic_size/ROOMS_ON_SIDE)
    if(max_side_id*ROOMS_ON_SIDE==allPublic_size):
        max_side_id-=1

    if start_index+1>allPublic_size and allPublic_size!=0:
        return render(request, 'chat/error.html')

    if start_index==0:
        first=True

    if start_index+ROOMS_ON_SIDE>allPublic_size:
        rooms=allPublic[start_index:allPublic_size]
    else:
        rooms=allPublic[start_index:start_index+ROOMS_ON_SIDE]
        next=True

    return render(request, 'request/allpublicroom.html', {
        'rooms': rooms,
        'id_page':id_side,
        'next': next,
        'first':first,
        'max_side_id': max_side_id,
        'error': error,
    })