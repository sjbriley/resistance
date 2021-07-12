from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame
from django.contrib.auth.decorators import login_required
from online.models import CustomUser, OnlineGames
from local.models import LocalGames

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

def leaderboards(request):
    games = LocalGames.objects.all()
    users = CustomUser.objects.all()
    leaderboard = {}
    for user in users:
        print('username: ' + str(user.username))
        leaderboard[user.username] = {}
        leaderboard[user.username]['gamesPlayed'] = 0
        games = LocalGames.objects.filter(players=user)
        for game in games:
            print('gameID: ' + str(game.gameID))
            leaderboard[user.username]['gamesPlayed'] += 1
            # check if user won and add to count
            # can check to see what roles user won as
    return render(request, 'leaderboards.html', {'leaderboard': leaderboard})

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
            try:
                game = OnlineGames.objects.filter(gameID__iexact=gameID)[0]
                if game.get_active():
                    return redirect('online_game', gameID = gameID)
            except:
                pass
    return render(request, 'online/home_online.html', {'form': form})

@login_required
def online_game_set_up(request):
    form = GameForm()
    import random, string
    gameID = ''.join([random.choice(string.ascii_uppercase.replace('O','') + string.digits.replace('0','')) for _ in range(6)])
    game = OnlineGames(gameID=gameID)
    game.save()
    return render(request, 'online/online_game_set_up.html', {'form': form, 'gameID': gameID})
    
@login_required
def online_game(request, gameID):
    try:
        game = OnlineGames.objects.filter(gameID__iexact=gameID)[0]
    except:
        return redirect('home_online')
    if not game.get_active():
        return redirect('home_online')
    game.players.add(request.user)
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