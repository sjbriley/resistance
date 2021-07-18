from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame, ChangeName
from django.contrib.auth.decorators import login_required
from online.models import CustomUser, OnlineGames
from local.models import LocalGames

# from django.template.defaulttags import register
# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(key)

def home_page(request):
    """Passes form for user to allow thme to sign in, along with their full name for display"""
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
                return render(request, 'home.html', {'game_form':game_form,'login_form':login_form, 'full_name': full_name})
            else:
                return render(request, 'home.html', {'game_form':game_form,'login_form':login_form, 'userError':'User does not exist.'})
        else:
            print(login_form.errors)
    if request.user.is_authenticated:
        full_name = request.user.get_full_name()
        leaderboard = {}
        user = request.user
        leaderboard[user.username] = {}
        for stat in ('gamesPlayed', 'wins', 'losses', 'resistanceWins', 'spyWins',
                     'resistanceLosses', 'spyLosses', 'jesterWins', 'puckWins', 'lancelotWins',
                     'merlinWins'):
            leaderboard[user.username][stat] = 0
        games = LocalGames.objects.filter(players=user)
        leaderboard = get_leaderboard_info(games, user, leaderboard)
        data = leaderboard[user.username]
    else:
        full_name = ''
        data = ''
    return render(request, 'home.html', {'data':data,'game_form':game_form,'login_form':login_form, 'full_name': full_name})

def help(request):
    return render(request, 'help.html')

def about(request):
    return render(request, 'about.html')


def sign_up(request):
    """passes form to user allowing for signing up"""
    form = CustomAuthenticationForm()
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name'].capitalize()
            last_name = form.cleaned_data['last_name'].capitalize()
            print(first_name)
            user = CustomUser.objects.create_user(username = username, password = '', first_name=first_name, last_name=last_name)
            user.is_active = True
            login(request, user)
            return redirect(reverse('home_page'))
        else:
            print(form.errors)
    return render(request, 'registration/sign_up.html', {'form':form})

def leaderboards(request):
    """Gathers ALL users in database and processes their games and results"""
    games = LocalGames.objects.all()
    users = CustomUser.objects.all()
    leaderboard = {}
    sortedLeaderboardList = []
    for user in users:
        sortedLeaderboardList.append(user.username)
        leaderboard[user.username] = {}
        for stat in ('gamesPlayed', 'wins', 'losses', 'resistanceWins', 'spyWins',
                     'resistanceLosses', 'spyLosses', 'jesterWins', 'puckWins', 'lancelotWins',
                     'merlinWins'):
            leaderboard[user.username][stat] = 0
        games = LocalGames.objects.filter(players=user)
        leaderboard = get_leaderboard_info(games, user, leaderboard)
        
    sortedLeaderboardList = sorted(sortedLeaderboardList, key=lambda x: leaderboard[x]['wins'])
    return render(request, 'leaderboards.html', {
        'leaderboard': leaderboard, 
        'sortedLeaderboardList': sortedLeaderboardList
        })

@login_required
def my_account(request):
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
def home_online(request):
    """Allows user to enter game ID or start a new game"""
    form = JoinExistingGame()
    if request.method == 'POST':
        form = JoinExistingGame(data=request.POST)
        if form.is_valid():
            game_id = form.cleaned_data['game_id'].upper()
            try:
                game = OnlineGames.objects.filter(game_id__iexact=game_id)[0]
                if game.get_active():
                    return redirect('online_game', game_id = game_id)
            except:
                pass
    return render(request, 'online/home_online.html', {'form': form})

@login_required
def online_game_set_up(request):
    """Allows host to set up game with their settings"""
    form = GameForm()
    import random, string
    game_id = ''.join([random.choice(string.ascii_uppercase.replace('O','') + string.digits.replace('0','')) for _ in range(6)])
    game = OnlineGames(game_id=game_id)
    game.save()
    return render(request, 'online/online_game_set_up.html', {'form': form, 'game_id': game_id})
    
@login_required
def online_game(request, game_id):
    """Game page for online games"""
    try:
        game = OnlineGames.objects.filter(game_id__iexact=game_id)[0]
    except:
        return redirect('home_online')
    if not game.get_active():
        return redirect('home_online')
    game.players.add(request.user)
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.getRoles()
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            return render(request, 'online/online_game.html', {'game_id': game_id, 'settings': settings})
        else:
            return render(request, 'online/online_game_set_up.html', {'form': form, 'game_id': game_id})
    return render(request, 'online/online_game.html', {'game_id': game_id})

def get_leaderboard_info(games, user, leaderboard):
    """Returns information for the leaderboards page and my_account
    Searches games that user was in and compiles information
    """
    leaderboard[user.username]['full_name'] = user.get_full_name()
    for game in games:
        if game.get_lobby_setup() == True: continue # was the game not finished and/or still in progress?
        info = game.get_user_leaderboard_info(user.username)
        leaderboard[user.username]['games_player'] += 1
        if info[0] == False:
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
                if info[2] == 'puck':
                    leaderboard[user.username]['puck_wins'] += 1
                if info[2] == 'lancelot':
                    leaderboard[user.username]['lancelot_wins'] += 1
                if info[2] == 'merlin':
                    leaderboard[user.username]['merlin_wins'] += 1
    try:
        leaderboard[user.username]['win_percentage'] = round(leaderboard[user.username]['wins'] / leaderboard[user.username]['gamesPlayed'] * 100, 1)
    except ZeroDivisionError:
        leaderboard[user.username]['win_percentage'] = 'N/A'
    return leaderboard