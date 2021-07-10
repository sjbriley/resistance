from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
# Create your models here.

    
class GameLog(models.Model):
    
    CHOICES = (('e', 'enabled'), ('d', 'disabled'))
    jester = forms.ChoiceField(label="Jester", widget=forms.RadioSelect, choices=CHOICES)
    merlin = forms.ChoiceField(label="merlin", widget=forms.RadioSelect, choices=CHOICES)
    assasin = forms.ChoiceField(label="assasin", widget=forms.RadioSelect, choices=CHOICES)
    puck = forms.ChoiceField(label="puck", widget=forms.RadioSelect, choices=CHOICES)
    
    
    # gameID = models.CharField(max_length=100)
    # rounds = models.CharField(max_length=100)
    # winner = models.CharField(max_length=100)
    # variables = models.CharField(max_length=100)
    # variables = models.CharField(max_length=100)
    # variables = models.CharField(max_length=100)
    
    # games = models.ManyToManyField("self")
    
    
class CustomUser(AbstractUser):
    
    def __str__(self):
        return self.username