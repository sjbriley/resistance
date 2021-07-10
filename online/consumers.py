import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# def ws_connect(message):
#     Group('users').add(message.reply_channel)


# def ws_disconnect(message):
#     Group('users').discard(message.reply_channel)
    
    

class GameConsumer(WebsocketConsumer):
    
    def connect(self):
        self.gameID = self.scope['url_route']['kwargs']['gameID']
        self.sheet_group_name = 'sheet_%s' % self.gameID

        # Join sheet group
        async_to_sync(self.channel_layer.group_add)(
            self.sheet_group_name,
            self.channel_name
        )
        print('connected')
        self.accept()

    def disconnect(self, close_code):
        # Leave sheet group
        async_to_sync(self.channel_layer.group_discard)(
            self.sheet_group_name,
            self.channel_name
        )
        print('disconected')

    # Receive message from WebSocket
    def receive(self, text_data):
        print('got data ' + str(text_data))
        text_data_json = json.loads(text_data)
        # Send gameID to sheet group
        async_to_sync(self.channel_layer.group_send)(
            self.sheet_group_name,
            {
                'type': 'refresh_sheet',
                'gameID': text_data_json['gameID'],
                'message': text_data_json['gameID'],
                'username': text_data_json['username'],
            }
        )

    # Receive message from sheet group
    def refresh_sheet(self, event):
        # Send gameID to WebSocket
        print('got refresh_sheet, event: ' + str(event))
        self.send(text_data=json.dumps({
            'gameID': event['gameID'],
            'message': event['message'],
            'username': event['username'],
        }))