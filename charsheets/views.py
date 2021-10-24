from charsheets.forms import CharacterForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Character

# Home, sweet home
def home(request):
    return render(request, 'charsheets/home.html')

# Zerżnięta z sieci templatka
def signupuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): #fajna sztuczka
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect(menu)

    else:
        form = UserCreationForm()

    return render(request, 'charsheets/signupuser.html', {'form': form})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect(home)

def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:            
            login(request, user)
            return redirect(menu)
    else:
        form = AuthenticationForm()
    return render(request, 'charsheets/loginuser.html', {'form': form})

# tworzenie postaci z forma opartego na modelu
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

def menu(request):
    characters = Character.objects.filter(user=request.user)
    return render(request, 'charsheets/menu.html', {'characters':characters})

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