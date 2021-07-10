from django.contrib import admin
from django.urls import path
from online import views as online_views
from django.conf.urls import include, url


urlpatterns = [
    path('', online_views.home_online, name='home_online'),
]