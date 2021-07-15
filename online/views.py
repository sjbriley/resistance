from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame
from django.contrib.auth.decorators import login_required
from online.models import CustomUser, OnlineGames
from local.models import LocalGames

# from django.template.defaulttags import register
# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(key)

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

def help(request):
    return render(request, 'help.html')

def about(request):
    return render(request, 'about.html')


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
    return render(request, 'my_account.html', {'data':data})

@login_required
def home_online(request):
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
    form = GameForm()
    import random, string
    game_id = ''.join([random.choice(string.ascii_uppercase.replace('O','') + string.digits.replace('0','')) for _ in range(6)])
    game = OnlineGames(game_id=game_id)
    game.save()
    return render(request, 'online/online_game_set_up.html', {'form': form, 'game_id': game_id})
    
@login_required
def online_game(request, game_id):
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