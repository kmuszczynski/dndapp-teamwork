from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CreateRequestAddToRoomForm
from chat.models import UserBelongsToRoom, ChatRoom
from .models import UserToRoomRequest

# Create your views here.

@login_required
def request_add_user_to_room(request, room_name):
    error=None
    if request.method=='POST':
        form = CreateRequestAddToRoomForm(request.POST)
        if form.is_valid():
            user_belongs = UserBelongsToRoom.objects.filter(room__name=room_name).filter(user=request.user)
            user_request = UserToRoomRequest.objects.filter(room__name=room_name).filter(user=request.user)
            room = ChatRoom.objects.get(name=room_name)

            if len(user_belongs)!=0:
                error="You already belongs to this room!!!"
            elif len(user_request)!=0:
                error="You have already sent request!!!"
            elif request.user == room.gamemaster:
                error="You are gamemaster in this room!!!"
            else:
                new_request = form.save(commit=False)
                new_request.room = room
                new_request.user = request.user
                new_request.save()
                return redirect('home')
    else:
        form = CreateRequestAddToRoomForm()

    return render(request, 'request/add_user_to_room_request.html', {'form': form, 'room':room_name, 'error': error})

@login_required
def view_all_request(request):
    requests=UserToRoomRequest.objects.filter(room__gamemaster=request.user)
    if request.method == 'POST':
        get_request = UserToRoomRequest.objects.get(pk=int(request.POST.get("request_id")))
        if request.POST.get("status") == "accept":
            UserBelongsToRoom.objects.create(room=get_request.room, user=get_request.user)
        get_request.delete()
    return render(request, 'request/all_request.html', {'requests': requests})

@login_required
def more_info_about_request_user_to_room(request, request_pk):
    get_request=UserToRoomRequest.objects.get(pk=request_pk)
    if request.method == 'POST':
        if request.POST.get("status") == "accept":
            UserBelongsToRoom.objects.create(room=get_request.room, user=get_request.user)
        get_request.delete()
        return redirect('viewallrequest')
    return render(request, 'request/more_about_request.html', {'request': get_request})

@login_required
def view_all_gameroom(request):
    gm_rooms=ChatRoom.objects.filter(gamemaster=request.user)
    player_rooms=UserBelongsToRoom.objects.filter(user=request.user)

    return render(request, 'request/all_player_room.html', {
        'gm_rooms': gm_rooms,
        'player_rooms': player_rooms,
    })

@login_required
def all_public_room(request, id_side):
    next=False
    first=False
    error=None

    if request.method=='POST':
        #Wpisanie nowego indexu strony
        if request.POST.get('id_new_side'):
            return redirect('allPublicRooms', id_side=request.POST.get('id_new_side'))
        #Uzycie pola szukaj
        elif request.POST.get('search'):
            room_search_name=request.POST.get('search')
            try:
                room = ChatRoom.objects.get(name=room_search_name)
                if room.gamemaster == request.user:
                    error="You are gamemaster in this room"
                else: 
                    return redirect('addrequest', room_name=room)
            except ChatRoom.DoesNotExist:
                error="There is no room with that name"
        #Klikniecie guzika od stworzenie requesta
        elif request.POST.get('room'):
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