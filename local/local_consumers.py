import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from local.models import LocalGames

class GameConsumer(WebsocketConsumer):

    def __init__(self,*args, **kwargs):
        super(GameConsumer, self).__init__(*args, **kwargs)
        # create self.username?
        
    def connect(self):
        self.gameID = self.scope['url_route']['kwargs']['gameID']
        self.game = LocalGames.objects.filter(gameID__iexact=self.gameID)[0]
        self.game_group_name = 'gameID_%s' % self.gameID

        # Join game group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave game group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # receive the data
        text_data_json = json.loads(text_data)
        
        # set the settings of the game if it is host joining
        if 'host' in text_data_json and 'init' in text_data_json:
            if text_data_json['host'] == True:
                if text_data_json['init'] == True:
                    self.game.set_settings(text_data_json['settings'])
                    
        # send players their role information since game has started and tell them gameStarted = True
        if 'gameStarted' in text_data_json:
            if text_data_json['gameStarted'] == True:
                user_roles = self.game.start_game()
                if user_roles != False:
                    async_to_sync(self.channel_layer.group_send)(
                        self.game_group_name,
                        {'type': 'refresh_game', 'userRoles': user_roles, 'gameStarted': True,}
                    )
                    
        if 'newUserJoined' in text_data_json:
            players = self.game.get_players()
            async_to_sync(self.channel_layer.group_send)(
                        self.game_group_name,
                        {'type': 'refresh_game', 'players': players, 'newUserJoined': True}
                    )
        if 'gameFinished' in text_data_json and 'winner' in text_data_json:
            if text_data_json['gameFinished'] == True:
                winner = text_data_json['winner']
                if winner == 'spies':
                    self.game.finish_game('spies')
                else:
                    self.game.finish_game('resistance')
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name,
                    {'type': 'refresh_game', 'gameFinished': True, 'winner': winner}
                )
            
    # Receive message and send to group. All keys must be in this function
    def refresh_game(self, event):
        self.send(text_data=json.dumps({
            'gameID': event['gameID'] if 'gameID' in event else None,
            'players': event['players'] if 'players' in event else None,
            'username': event['username'] if 'username' in event else None,
            'init': event['init'] if 'init' in event else None,
            'host': event['host'] if 'host' in event else None,
            'userRoles': event['userRoles'] if 'userRoles' in event else None,
            'settings': event['settings'] if 'settings' in event else None,
            'gameStarted': event['gameStarted'] if 'gameStarted' in event else None,
            'newUserJoined': event['newUserJoined'] if 'newUserJoined' in event else None,
            'gameFinished': event['gameFinished'] if 'gameFinished' in event else None,
            'winner': event['winner'] if 'winner' in event else None,
        }))