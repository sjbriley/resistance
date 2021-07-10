from django.contrib import admin
from django.urls import path
from online import views as online_views
from django.conf.urls import include, url


urlpatterns = [
    path('', online_views.home_online, name='home_online'),
    path('new_game/', online_views.online_game_set_up, name='new_game_set_up'),
    path('ws/game/<str:gameID>/', online_views.online_game, name="online_game"),
]