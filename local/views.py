from django.shortcuts import redirect, render
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame
from django.contrib.auth.decorators import login_required
from online.models import CustomUser
from local.models import LocalGames

@login_required
def home_local(request):
    """Home page for local games, allows user to enter game ID or start a new game"""
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
    """Send GameForm to local game set up page to allow for settings of game to be choosen, and create the game ID randomly"""
    form = GameForm()
    import random, string
    game_id = ''.join(([random.choice(string.ascii_uppercase.replace('O','') + string.digits.replace('0','')) for _ in range(6)]))
    game = LocalGames(game_id=game_id)
    game.save()
    return render(request, 'local/local_game_set_up.html', {'form': form, 'game_id': game_id})

@login_required
def local_game(request, game_id):
    """ Renders the game page
    If the method is POST, then it is the host coming from local_game_set_up
        - pass Settings to the game
    If not post, then it is user joining with a game ID from local_homes
    """
    try:
        game = LocalGames.objects.filter(game_id__iexact=game_id)[0]
    except:
        return redirect('home_local')
    if game.get_lobby_setup() == False:
        return redirect('home_local')
    game.players.add(request.user)
    request.user.local_games.add(game)
    full_name = request.user.get_full_name()
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.getRoles()
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            return render(request, 'local/local_game.html', {'full_name': full_name,'game_id': game_id, 'settings': settings})
        else:
            return render(request, 'local/local_game_set_up.html', {'form': form, 'game_id': game_id})
    return render(request, 'local/local_game.html', {'full_name': full_name, 'game_id': game_id})