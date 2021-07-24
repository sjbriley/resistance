from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

    

    
class CustomUser(AbstractUser):

    # we do not need local_games or online_games since we use manyToManyField in our game models, with related_names
    # online_games = models.CharField(max_length=1000)
    # local_games = models.CharField(max_length=3000)
    first_name = models.CharField(max_length=25, unique=False)
    last_name = models.CharField(max_length=25, unique=False)
        
    def __str__(self):
        return self.username
    
    def get_games(self):
        return self.local_games.all()
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def change_name(self, first_name, last_name):
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
   
class OnlineGames(models.Model):
    game_id = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    players = models.ManyToManyField('online.CustomUser', related_name = 'online_games') # a list of usernames
    roles = models.CharField(max_length=5000)
    settings = models.CharField(max_length=1000)
    num_players = models.CharField(max_length=2)
    winning_team = models.CharField(max_length=50)
    in_session = models.BooleanField(default=False)
    
    def get_lobby_setup(self):
        """Return if the lobby is in lobby or not"""
        if self.is_active == False or self.in_session == True:
            return False
        return True
    
"""
To create relationships using ManyToManyField:
    1. creaate user
    2. save user 
        userA.save()
    3. create gamelog and to user 
        game = GameLog
        game.save()
        userA.add(gameLog)
        
    Assumes User has 'games = models.ManyToManyField(GameLog)' and 
    GameLog has 'user = models.CharField'
    Saving gamelog to a user twice will not duplicate
    
    ex:
    
    game = GameLog()
    game.save()
    game2 = GameLog()
    game2.save()

    user = request.user
    user.games.add(game)
    user.games.add(game2)
    print(user.games.all())
"""