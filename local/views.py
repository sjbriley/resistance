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
            game_id = form.cleaned_data['game_id'].upper()
            try:
                game = LocalGames.objects.filter(game_id__iexact=game_id)[0]
                if game.get_lobby_setup():
                    return redirect('local_game', game_id = game_id)
            except:
                pass
    return render(request, 'local/home_local.html', {'form': form})

@login_required
def local_game_set_up(request):
    form = GameForm()
    import random, string
    game_id = ''.join(([random.choice(string.ascii_uppercase.replace('O','') + string.digits.replace('0','')) for _ in range(6)]))
    game = LocalGames(game_id=game_id)
    game.save()
    return render(request, 'local/local_game_set_up.html', {'form': form, 'game_id': game_id})

@login_required
def local_game(request, game_id):
    try:
        game = LocalGames.objects.filter(game_id__iexact=game_id)[0]
    except:
        return redirect('home_local')
    if game.get_lobby_setup() == False:
        return redirect('home_local')
    game.players.add(request.user)
    request.user.local_games.add(game)
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.getRoles()
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            return render(request, 'local/local_game.html', {'game_id': game_id, 'settings': settings})
        else:
            return render(request, 'local/local_game_set_up.html', {'form': form, 'game_id': game_id})
    return render(request, 'local/local_game.html', {'game_id': game_id})