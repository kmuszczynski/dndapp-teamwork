from charsheets.forms import CharacterForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import Character
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'charsheets/profile.html')

# tworzenie postaci z forma opartego na modelu
@login_required
def createchar(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            newCharacter = form.save(commit=False)
            newCharacter.user = request.user
            newCharacter.save()
            return redirect(menu)
    else:
        form = CharacterForm()
    return render(request, 'charsheets/createchar.html', {'form': form})

@login_required
def menu(request):
    characters = Character.objects.filter(user=request.user)
    return render(request, 'charsheets/menu.html', {'characters':characters})

@login_required
def viewcharacter(request, character_pk):
    character = get_object_or_404(Character, pk=character_pk, user=request.user) #też śmieszna sztuczka
    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            # return redirect(menu)
    else:
        form = CharacterForm(instance=character)
    return render(request, 'charsheets/viewcharacter.html', {'character':character, 'form':form})