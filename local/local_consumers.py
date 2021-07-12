import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    
    def connect(self):
        self.gameID = self.scope['url_route']['kwargs']['gameID']
        self.sheet_group_name = 'gameID_%s' % self.gameID

        # Join sheet group
        async_to_sync(self.channel_layer.group_add)(
            self.sheet_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave sheet group
        async_to_sync(self.channel_layer.group_discard)(
            self.sheet_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.sheet_group_name,
            {
                'type': 'refresh_sheet',
                'gameID': text_data_json['gameID'],
                'username': text_data_json['username'],
                'init': text_data_json['init'],
                'host': text_data_json['host'],
                'userRoles': text_data_json['userRoles'],
                'settings': text_data_json['settings'],
            }
        )

    # Receive message from sheet group
    def refresh_sheet(self, event):
        self.send(text_data=json.dumps({
            'gameID': event['gameID'],
            'username': event['username'],
            'init': event['init'],
            'host': event['host'],
            'userRoles': event['userRoles'],
            'settings': event['settings'],
        }))