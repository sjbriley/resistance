from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
# Create your models here.

    

    
class CustomUser(AbstractUser):

    games = models.ManyToManyField('GameLog')

    def __str__(self):
        return self.username
   
   
class GameLog(models.Model):
    
    user = models.CharField(max_length=30) 
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