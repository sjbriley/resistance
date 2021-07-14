from django.shortcuts import redirect, render
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame
from django.contrib.auth.decorators import login_required
from online.models import CustomUser
from local.models import LocalGames

@login_required
def home_local(request):
    form = JoinExistingGame()
    if request.method == 'POST':
        form = JoinExistingGame(data=request.POST)
        if form.is_valid():
            gameID = form.cleaned_data['gameID'].upper()
            try:
                game = LocalGames.objects.filter(gameID__iexact=gameID)[0]
                if game.get_lobby_setup():
                    return redirect('local_game', gameID = gameID)
            except:
                pass
    return render(request, 'local/home_local.html', {'form': form})

@login_required
def local_game_set_up(request):
    form = GameForm()
    import random, string
    gameID = ''.join(([random.choice(string.ascii_uppercase.replace('O','') + string.digits.replace('0','')) for _ in range(6)]))
    game = LocalGames(gameID=gameID)
    game.save()
    return render(request, 'local/local_game_set_up.html', {'form': form, 'gameID': gameID})

@login_required
def local_game(request, gameID):
    try:
        game = LocalGames.objects.filter(gameID__iexact=gameID)[0]
    except:
        return redirect('home_local')
    if game.get_lobby_setup() == False:
        return redirect('home_local')
    game.players.add(request.user)
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.getRoles()
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            return render(request, 'local/local_game.html', {'gameID': gameID, 'settings': settings})
        else:
            return render(request, 'local/local_game_set_up.html', {'form': form, 'gameID': gameID})
    return render(request, 'local/local_game.html', {'gameID': gameID})