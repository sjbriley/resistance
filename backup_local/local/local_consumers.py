import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from local.models import LocalGames
from local.game_logic import JESTER, \
                        MERLIN, \
                        PUCK, \
                        LANCELOT, \
                        UTHER, \
                        TRISTAN, \
                        ISEULT, \
                        ARTHUR, \
                        ASSASSIN, \
                        MORDRED, \
                        GUINEVERE, \
                        MORGANA, \
                        MAELAGANT, \
                        COLGREVANCE

class GameConsumer(WebsocketConsumer):

    def __init__(self,*args, **kwargs):
        super(GameConsumer, self).__init__(*args, **kwargs)
        # create self.username?
        
    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game = LocalGames.objects.filter(game_id__iexact=self.game_id)[0]
        self.game_group_name = 'game_id_%s' % self.game_id

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
                    
        # send players their role information since game has started and tell them game_started = True
        if 'game_started' in text_data_json:
            if text_data_json['game_started'] == True:
                user_roles = self.game.start_game()
                if user_roles != False:
                    async_to_sync(self.channel_layer.group_send)(
                        self.game_group_name,
                        {'type': 'refresh_game', 'user_roles': user_roles, 'game_started': True,}
                    )
                    
        if 'new_user_joined' in text_data_json:
            
            # DO CHECK HERE TO SEE IF GAME STARTED AND USER IS REFRESHING OR RE-JOINING
            
            players = self.game.get_players()
            async_to_sync(self.channel_layer.group_send)(
                        self.game_group_name,
                        {'type': 'refresh_game', 'players': players, 'new_user_joined': True}
                    )
        if 'game_finished' in text_data_json and 'winner' in text_data_json:
            if text_data_json['game_finished'] == True:
                winner = text_data_json['winner']
                if winner == 'spies':
                    self.game.finish_game('spies')
                else:
                    self.game.finish_game('resistance')
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name,
                    {'type': 'refresh_game', 'game_finished': True, 'winner': winner}
                )
            
    # Receive message and send to group. All keys must be in this function
    def refresh_game(self, event):
        self.send(text_data=json.dumps({
            'game_id': event['game_id'] if 'game_id' in event else None,
            'players': event['players'] if 'players' in event else None,
            'username': event['username'] if 'username' in event else None,
            'init': event['init'] if 'init' in event else None,
            'host': event['host'] if 'host' in event else None,
            'user_roles': event['user_roles'] if 'user_roles' in event else None,
            'settings': event['settings'] if 'settings' in event else None,
            'game_started': event['game_started'] if 'game_started' in event else None,
            'new_user_joined': event['new_user_joined'] if 'new_user_joined' in event else None,
            'game_finished': event['game_finished'] if 'game_finished' in event else None,
            'winner': event['winner'] if 'winner' in event else None,
        }))