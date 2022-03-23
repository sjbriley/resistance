from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame, ChangeName
from django.contrib.auth.decorators import login_required
from .models import CustomUser, OnlineGames
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from typing import Union
from .game_logic import GOOD_ROLES, BAD_ROLES, MIN_ASSASSIN, MAX_ASSASSIN

def home_page(request: HttpRequest) -> HttpResponse:
    """Passes form for user to allow thme to sign in, along with their full name for display.
    """
    login_form = CustomLoginForm()
    game_form = JoinExistingGame()
    if request.method == 'POST':
        login_form = CustomLoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            user = authenticate(username=username, password='')
            if user:
                login(request, user)
                full_name = request.user.get_full_name()
                return render(request, 'home.html',
                              {
                               'game_form':game_form,
                               'login_form':login_form,
                               'full_name': full_name
                               })
            else:
                return render(request, 'home.html',
                            {
                            'game_form':game_form,
                            'login_form':login_form,
                            'userError':'User does not exist.'
                            })
        else:
            print(login_form.errors)
    # get this users leaderboard information
    if request.user.is_authenticated:
        full_name = request.user.get_full_name()
        leaderboard = {}
        user = request.user
        leaderboard[user.username] = {}
        for stat in ('gamesPlayed', 'wins', 'losses',
                     'resistanceWins', 'spyWins',
                     'resistanceLosses', 'spyLosses',
                     'jesterWins', 'puckWins',
                     'lancelotWins', 'merlinWins'):
            leaderboard[user.username][stat] = 0
        games = OnlineGames.objects.filter(players=user)
        leaderboard = get_leaderboard_info(games, user, leaderboard)
        data = leaderboard[user.username]
    else:
        full_name = ''
        data = ''
    return render(request, 'home.html', 
                    {
                    'data':data,
                    'game_form':game_form,
                    'login_form':login_form,
                    'full_name': full_name
                    })

def game_information(request: HttpRequest) -> HttpResponse:
    return render(request, 'game_information/game_information.html')

def role_information(request: HttpRequest) -> HttpResponse:
    return render(request, 'game_information/role_information.html')

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def sign_up(request: HttpRequest) -> HttpResponse:
    """passes form to user allowing for signing up"""
    form = CustomAuthenticationForm()
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # password1 = form.cleaned_data['password1']
            # password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name'].capitalize()
            last_name = form.cleaned_data['last_name'].capitalize()
            user = CustomUser.objects.create_user(
                                                  username = username,
                                                  password = '',
                                                  first_name = first_name,
                                                  last_name = last_name
                                                  )
            user.is_active = True
            login(request, user)
            return redirect(reverse('home_page'))
        else:
            print(form.errors)
    return render(request, 'registration/sign_up.html', {'form':form})

def leaderboards(request: HttpRequest) -> HttpResponse:
    """Gathers ALL users in database and processes their games and results"""
    games = OnlineGames.objects.all()
    users = CustomUser.objects.all()
    leaderboard = {}
    sortedLeaderboardList = []
    for user in users:
        sortedLeaderboardList.append(user.username)
        leaderboard[user.username] = {}
        # initialize leaderboard dict with all users
        for stat in (
                     'gamesPlayed', 'wins', 'losses',
                     'resistanceWins', 'spyWins',
                     'resistanceLosses', 'spyLosses',
                     'jesterWins', 'puckWins',
                     'lancelotWins', 'merlinWins'
                     ):
            leaderboard[user.username][stat] = 0
        games = OnlineGames.objects.filter(players=user)
        # pass in games this user has participated in to update leaderboards
        leaderboard = get_leaderboard_info(games, user, leaderboard)
        
    sortedLeaderboardList = sorted(sortedLeaderboardList, key=lambda x: leaderboard[x]['wins'])
    return render(request, 'leaderboards.html', {
        'leaderboard': leaderboard, 
        'sortedLeaderboardList': sortedLeaderboardList
        })

@login_required
def my_account(request: HttpRequest) -> HttpResponse:
    """Access my_account page, pass in form allowing for first name/last name changing"""
    if request.method == 'POST':
        form = ChangeName(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = request.user
            user.change_name(first_name, last_name)
            user.save()
    else:
        form = ChangeName()
    user = request.user
    games = user.get_games()
    leaderboard = {}
    leaderboard[user.username] = {}
    for stat in ('gamesPlayed', 'wins', 'losses', 'resistanceWins', 'spyWins',
                     'resistanceLosses', 'spyLosses', 'jesterWins', 'puckWins', 'lancelotWins',
                     'merlinWins', 'winPercentage'):
            leaderboard[user.username][stat] = 0
    leaderboard = get_leaderboard_info(games, user, leaderboard)
    data = leaderboard[user.username]
    return render(request, 'my_account.html', {'data':data, 'form':form})

@login_required
def home_online(request: HttpRequest) -> HttpResponse:
    """Allows user to enter game ID or start a new game"""
    form = JoinExistingGame()
    if request.method == 'POST':
        form = JoinExistingGame(data=request.POST)
        if form.is_valid():
            game_id = form.cleaned_data['game_id'].upper()
            try:
                game = OnlineGames.objects.filter(game_id__iexact=game_id)[0]
                # if game is in lobby and players can join
                if game.get_lobby_setup():
                    return redirect('online_game', game_id = game_id)
                else:
                    print("Game not active")
            except Exception as e:
                print(e)
                print('Exception occured')
        else:
            print('form not valid')
    messages.add_message(request, messages.ERROR, 'Game ID not valid')
    return redirect(reverse('home_page'))

@login_required
def online_game_set_up(request: HttpRequest) -> HttpResponse:
    """Allows host to set up game with their settings.
    Generate a random 6 digit ID and save the game to db.    
    """
    form = GameForm()
    import random, string
    # generate a 6 digit game ID with numbers and uppercase letters
    game_id = ''.join([random.choice(string.ascii_uppercase.replace('O','')
                                     + string.digits.replace('0','')) for _ in range(6)])
    game = OnlineGames(game_id=game_id)
    game.save()
    return render(
        request,
        'online/online_game_set_up.html',
        {
            'form': form,
            'game_id': game_id,
            'good_roles': GOOD_ROLES,
            'bad_roles': BAD_ROLES,
        })
    
@login_required
def online_game(request: HttpRequest, game_id: int) -> HttpResponse:
    """Game page for online games"""
    try:
        game = OnlineGames.objects.filter(game_id__iexact=game_id)[0]
    except:
        return redirect('home_online')
    if not game.get_lobby_setup():
        return redirect('home_online')
    game.players.add(request.user)
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.get_roles()
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            settings[MIN_ASSASSIN] = form.cleaned_data[MIN_ASSASSIN]
            settings[MAX_ASSASSIN] = form.cleaned_data[MAX_ASSASSIN]
            print(settings)
            return render(request, 'online/online_game.html',
                          {
                          'game_id': game_id,
                          'settings': settings
                          })
        else:
            return render(request, 'online/online_game_set_up.html',
                                            {
                                            'form': form,
                                            'game_id': game_id
                                            })
    return render(request, 'online/online_game.html', {'game_id': game_id})

def get_leaderboard_info(games: QuerySet, user: CustomUser, leaderboard: dict) -> dict:
    """Returns information for the leaderboards page and my_account
    Searches games that user was in and compiles information

    Args:
        games (QuerySet): contains all games that user played in
        user (CustomUser): current user
        leaderboard: dict
        
    Returns:
        dict: updated leaderboard info
        
    """
    leaderboard[user.username]['full_name'] = user.get_full_name()
    for game in games:
        # was the game not finished and/or still in progress?
        if game.get_lobby_setup() is True:
            continue
        info = game.get_user_leaderboard_info(user.username)
        leaderboard[user.username]['games_player'] += 1
        if info[0] is False:
            leaderboard[user.username]['losses'] += 1
            if info[1] == 'spy':
                leaderboard[user.username]['spy_losses'] += 1
            else:
                leaderboard[user.username]['resistance_losses'] += 1
        else:
            leaderboard[user.username]['wins'] += 1
            if info[1] == 'spy':
                leaderboard[user.username]['spy_wins'] += 1
            else:
                leaderboard[user.username]['resistance_wins'] += 1
                if info[2] == 'jester':
                    leaderboard[user.username]['jester_wins'] += 1
                elif info[2] == 'puck':
                    leaderboard[user.username]['puck_wins'] += 1
                elif info[2] == 'lancelot':
                    leaderboard[user.username]['lancelot_wins'] += 1
                elif info[2] == 'merlin':
                    leaderboard[user.username]['merlin_wins'] += 1
    try:
        leaderboard[user.username]['win_percentage'] = round(
            leaderboard[user.username]['wins'] / leaderboard[user.username]['gamesPlayed'] * 100, 1
            )
    except ZeroDivisionError:
        leaderboard[user.username]['win_percentage'] = 'N/A'
    return leaderboard