from chat.models import CharacterBelongsToRoom

def create_CharacterBelongsToRoom(getRequest):
    user_characters=CharacterBelongsToRoom.objects.filter(room=getRequest.room)
    if len(user_characters)==0:
        CharacterBelongsToRoom.objects.create(room=getRequest.room, character=getRequest.character, status=1)
    else:
        user_characters=CharacterBelongsToRoom.objects.filter(room=getRequest.room).filter(character__user=getRequest.character.user)
        if len(user_characters)==0:
            CharacterBelongsToRoom.objects.create(room=getRequest.room, character=getRequest.character, status=1)
        else:
            CharacterBelongsToRoom.objects.create(room=getRequest.room, character=getRequest.character, status=2)