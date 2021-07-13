from django.db import models
from online.models import CustomUser
import json

# Create your models here.
class LocalGames(models.Model):
    gameID = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    players = models.ManyToManyField('online.CustomUser') # a list
    numPlayers = models.CharField(max_length=2)
    settings = models.CharField(max_length=1000)
    
    def get_active(self):
        return self.is_active
    
    def get_players(self):
        playerSet = set()
        for player in self.players.all():
            playerSet.add(player.username)
        self.numPlayers = str(len(playerSet))
        return playerSet

    def get_user_leaderboard_info(self, player):
        player = CustomUser.objects.filter(username__iexact=player)[0]
        return [True, 'resistance', 'jester']
    
    def add_player(self, player):
        player = CustomUser.objects.filter(username__iexact=player)[0]
        self.players.add(player) # will not duplicate
        
    def set_settings(self, settings):
        # assumes it is a dictionary -> converts it to a string
        self.settings = json.dumps(settings)
        
    def start_game(self):
        players = self.get_players()
        if len(players) > 10 or len(players) < 5:
            return
        if self.settings == '':
            return
        # info = getInfo(self.numPlayers, players, settings)
""" 
user = CustomUser(username='test')
user.save()
game = LocalGames()
game.save()
game.players.add(user) <- can add many players

to filter games for a specific user:
results = LocalGames.objects.filter(players=CustomUser.objects.filter(username='test')[0])
or if user is known
results = LocalGames.objects.filter(players=user)
This will return query set of all games that the user is in

to get all players in a game:
game.players.all()

"""