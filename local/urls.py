from django.contrib import admin
from django.urls import path
from local import views as local_views
from django.conf.urls import include, url


urlpatterns = [
    path('', local_views.home_local, name='home_local'),
]