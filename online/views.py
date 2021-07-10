from django.shortcuts import redirect, render
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from online.forms import customAuthenticationForm, customLoginForm, GameForm
from django.contrib.auth.decorators import login_required
from online.models import CustomUser

# Create your views here.

def home_page(request):
    form = customLoginForm()
    if request.method == 'POST':
        form = customLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = authenticate(username=username, password='')
            if user:
                login(request, user)
                return render(request, 'home.html', {'form':form})
            else:
                return render(request, 'home.html', {'form':form, 'userError':'User does not exist.'})
        else:
            print(form.errors)
    return render(request, 'home.html', {'form':form})

def home_online(request):
    return render(request, 'online/home_online.html')

def sign_up(request):
    form = customAuthenticationForm()
    if request.method == 'POST':
        form = customAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = CustomUser.objects.create_user(username = username, password = '')
            user.is_active = True
            login(request, user)
            return redirect(reverse('home_page'))
        else:
            print(form.errors)
    return render(request, 'registration/sign_up.html', {'form':form})

@login_required
def my_account(request):
    return render(request, 'my_account.html')

@login_required
def online_game_set_up(request):
    form = GameForm()
    if request.method == 'POST':
        import random, string
        gameID = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(6)])
        return render(request, 'online/online_game_set_up.html', {'form': form, 'gameID': gameID})
    return render(request, 'online/online_game_set_up.html', {'form': form})
    
@login_required
def online_game(request, gameID):
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            settings = form.cleaned_data['settings']
            return render(request, 'online/online_game.html', {'gameID': gameID, 'settings': settings})
    return redirect('online_game', gameID = gameID)