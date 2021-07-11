from django.shortcuts import redirect, render
from django.urls import reverse
from online.forms import CustomAuthenticationForm, CustomLoginForm, GameForm, JoinExistingGame
from django.contrib.auth.decorators import login_required
from online.models import CustomUser, GameLog

@login_required
def home_local(request):
    form = JoinExistingGame()
    if request.method == 'POST':
        form = JoinExistingGame(data=request.POST)
        if form.is_valid():
            gameID = form.cleaned_data['gameID'].upper()
            # do check to see if game exists
            return redirect('local_game', gameID = gameID)
    return render(request, 'local/home_local.html', {'form': form})

@login_required
def local_game_set_up(request):
    form = GameForm()
    import random, string
    gameID = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(6)])
    return render(request, 'local/local_game_set_up.html', {'form': form, 'gameID': gameID})

@login_required
def local_game(request, gameID):
    if request.method == 'POST':
        form = GameForm(data=request.POST)
        if form.is_valid():
            roles = form.getRoles()
            print('got roles' + str(roles))
            settings = {}
            for role in roles:
                settings[role] = form.cleaned_data[role]
            return render(request, 'local/local_game.html', {'gameID': gameID, 'settings': settings})
        else:
            return render(request, 'local/local_game.html', {'form': form, 'gameID': gameID})
    return render(request, 'local/local_game.html', {'gameID': gameID})