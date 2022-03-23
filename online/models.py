from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import QuerySet
from django.dispatch import receiver
from typing import Tuple, Union
import json
from .game_logic import create_game_logic
    
class CustomUser(AbstractUser):

    # we do not need online_games or online_games since we use manyToManyField in our game models, with related_names
    # online_games = models.CharField(max_length=1000)
    # online_games = models.CharField(max_length=3000)
    first_name = models.CharField(max_length=25, unique=False)
    last_name = models.CharField(max_length=25, unique=False)
        
    def __str__(self) -> str:
        return self.username
    
    def get_games(self) -> QuerySet:
        return self.online_games.all()
    
    def get_first_name(self) -> str:
        return self.first_name
    
    def get_last_name(self) -> str:
        return self.last_name
    
    def get_full_name(self) -> str:
        return self.first_name + ' ' + self.last_name
    
    def change_name(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
   
class OnlineGames(models.Model):
    game_id = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    players = models.ManyToManyField('online.CustomUser', related_name = 'online_games') # related_name allows for accesing Games through players with '.games' instead of using 'games_set'
    roles = models.CharField(max_length=5000)
    settings = models.CharField(max_length=1000)
    num_players = models.CharField(max_length=2)
    winning_team = models.CharField(max_length=50)
    in_session = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        print(type(self.game_id))
        return self.game_id
    
    def get_lobby_setup(self):
        """Return if the lobby is in lobby or not"""
        # if self.is_active == False or self.in_session == True:
        #     return False
        return True
    
    def get_players(self) -> list:
        """Get a list of players. 
        If two users are in game with same first name, it adds last initial
        If the two users have same last initial, it sends full last name

        Returns:
            list: list of players in game 
        """
        player_list = {}
        for player in self.players.all():
            if player.get_first_name() not in player_list.keys():
                player_list[player.get_first_name()] = player.username
            else:
                existing_player = player_list[player.get_first_name()]
                user_with_same_name = CustomUser.objects.filter(username__iexact=existing_player)[0]
                del player_list[player.get_first_name()]
                if user_with_same_name.get_last_name()[0] != user_with_same_name.get_last_name()[0]:
                    player_list[user_with_same_name.get_first_name() + user_with_same_name.get_last_name()[0]] = user_with_same_name
                    player_list[player.get_first_name() + player.get_last_name()[0]] = player.username
                else:
                    player_list[user_with_same_name.get_full_name()] = user_with_same_name
                    player_list[player.get_full_name()] = player.username
        self.num_players = str(len(player_list))
        return list(player_list.keys())

    def get_user_leaderboard_info(self, player: str) -> Tuple[bool, str, str]:
        """Returns games results for a particular player
        Reurns [won, team, role]
        """
        player = CustomUser.objects.filter(username__iexact=player)[0]
        return (True, 'resistance', 'jester')
    
    def add_player(self, player: str) -> None:
        player = CustomUser.objects.filter(username__iexact=player)[0]
        self.players.add(player) # will not duplicate
    
    def remove_player(self, player: str) -> None:
        player = CustomUser.objects.filter(username__iexact=player)[0]
        self.players.remove(player) # will not duplicate
        
    def set_settings(self, settings: dict) -> None:
        # assumes it is a dictionary -> converts it to a string
        self.settings = json.dumps(settings)
        
    def start_game(self) -> Union[dict, bool]:
        """Begins the game
        
        Returns:
            dict | bool: false if unsuccesful, otherwise the game info
            
        """
        players = self.get_players()
        self.in_session = True
        if len(players) > 10 or len(players) < 5:
            return False
        if self.settings == '':
            return False
        info = create_game_logic(players, self.settings)
        self.roles = json.dumps(info)
        if info:
            return info
        else:
            return False
    
    def finish_game(self, team: str) -> None:
        self.is_active = False
        self.winning_team = team
        self.in_session = False
    
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