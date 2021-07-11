from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame
from django.contrib.auth.decorators import login_required
from online.models import CustomUser, GameLog

# Create your views here.

def home_page(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
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

def sign_up(request):
    form = CustomAuthenticationForm()
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
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
def home_online(request):
    form = JoinExistingGame()
    if request.method == 'POST':
        form = JoinExistingGame(data=request.POST)
        if form.is_valid():
            gameID = form.cleaned_data['gameID'].upper()
            # do check to see if game exists
            return redirect('online_game', gameID = gameID)
    return render(request, 'online/home_online.html', {'form': form})

@login_required
def online_game_set_up(request):
    form = GameForm()
    import random, string
    gameID = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(6)])
    return render(request, 'online/online_game_set_up.html', {'form': form, 'gameID': gameID})
    
@login_required
def online_game(request, gameID):
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.getRoles()
            print('got roles' + str(roles))
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            return render(request, 'online/online_game.html', {'gameID': gameID, 'settings': settings})
        else:
            return render(request, 'online/online_game_set_up.html', {'form': form, 'gameID': gameID})
    return render(request, 'online/online_game.html', {'gameID': gameID})