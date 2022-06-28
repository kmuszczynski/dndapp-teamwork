from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage, ChatRoom, UserBelongsToRoom
from .forms import CreateRoomForm
from charsheets.models import Character
from grid.models import Grid, GridAreaWithCharacter

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
    gm = request.user == room.gamemaster
    user = UserBelongsToRoom.objects.filter(user=request.user).filter(room=room)
    if not room or (not user and not gm):
        return render(request, 'chat/error.html')

    chats = ChatMessage.objects.filter(room=room)

    characters = Character.objects.filter(room=room)

    current_grid = Grid.objects.filter(status=1).first()
    allGridAreaWithCharacters = GridAreaWithCharacter.objects.filter(grid=current_grid)

    grid=[]
    if current_grid:
        for i in range(current_grid.rows):
            row = []
            for j in range(current_grid.columns):
                gridAreaWithCharacters = GridAreaWithCharacter.objects.filter(grid=current_grid).filter(row=i).filter(column=j).first()
                if gridAreaWithCharacters:
                    color = gridAreaWithCharacters.color
                    count = 0
                    
                    for z in range(1, 6, 2):
                        if "89abcdef".find(color[z])!=-1:
                            count += 1

                    if count > 0:
                        text_color = "black"
                    else:
                        text_color = "white"

                    row.append([gridAreaWithCharacters.character, gridAreaWithCharacters.color, text_color])
                else:
                    row.append(["-", "-", "-"])
            
            grid.append(row)


    if not gm:
        playerCharacters = characters.filter(user=request.user)
        otherCharactersList = characters.exclude(user=request.user)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'gm': False,
            'chats': chats,
            'playerCharacters': playerCharacters,
            'otherCharactersList': otherCharactersList,
            'grid': grid,
        })
    else:
        grid_list = Grid.objects.filter(room=room)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'gm': True,
            'chats': chats,
            'playerCharacters': characters,
            'grid_list': grid_list,
            'grid': grid,
        })
