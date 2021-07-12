from django.urls import re_path
from django.conf.urls import url
from online import online_consumers
from local import local_consumers

websocket_urlpatterns = [
    re_path(r'online/wss/(?P<gameID>\w+)/$', online_consumers.GameConsumer.as_asgi()),
    re_path(r'local/wss/(?P<gameID>\w+)/$', local_consumers.GameConsumer.as_asgi()),
]