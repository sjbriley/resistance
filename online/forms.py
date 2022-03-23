from django.forms import ModelForm, Textarea
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from typing import Union

from .models import CustomUser, OnlineGames
from . import game_logic

roles = ()

class CustomAuthenticationForm(forms.Form):
    """Used for verifying account creation
    """
    username = forms.CharField(
                    max_length=30,
                    label="Username",
                    error_messages={'invalid': "Invalid Username"},
                    widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'placeholder': 'Choose a unique username',
                            'style': 'font-size:1.25rem;'
                            }))
    first_name = forms.CharField(
                    label="First Name",
                    error_messages={'invalid': "Invalid Name"},
                    widget=forms.TextInput(
                        attrs={'class':'form-control',
                                'placeholder': 'First Name',
                                'style': 'font-size:1.25rem;'
                                }))
    last_name = forms.CharField(
                    label="Last Name",
                    error_messages={'invalid': "Invalid Name"},
                    widget=forms.TextInput(
                        attrs={'class':'form-control',
                                'placeholder': 'Last Name',
                                'style': 'font-size:1.25rem;'
                                }))
    
    def clean_username(self) -> str:
        """Verifies the username does not already exists.
        Returns the username if not for creation.
        """
        existing = CustomUser.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',)
        
class CustomLoginForm(AuthenticationForm):
    """Used for verifying user exists when logging in
    """
    username = forms.CharField(
                max_length=30,
                label="Username",
                error_messages={'invalid': "Invalid Username"},
                widget=forms.TextInput(
                    attrs={'class':'form-control',
                            'placeholder': 'Enter your unique username',
                            'style': 'font-size:1.25rem;text-align:center;'
                            }))

    def __init__(self, *args, **kwargs) -> None:
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password']
    class Meta:
        model = CustomUser
        fields = ('username',)

class GameForm(forms.Form):
    
    # define format to be used for percentage forms
    format = forms.IntegerField(
                initial = 100,
                widget = forms.NumberInput(
                    attrs={
                        'class':'form-text',
                        'min': '0',
                        'max': '100',
                 }))
    jester = format
    merlin = format
    percival = format
    uther = format
    tristan = format
    iseult = format
    puck = format
    arthur = format
    lancelot = format
    guinevere = format
    mordred = format
    morgana = format
    maelagant = format
    colgrevance = format
    assassin = format
    # we need to verify all roles are listed here
    # and match with ALL_ROLES
    min_assassinable_roles = forms.IntegerField(
                label = 'Min # of Assassinable Roles',
                initial = 1,
                widget = forms.NumberInput(
                    attrs={
                        'class':'form-text',
                        'min': '0',
                        'max': '3',
                 }))
    max_assassinable_roles = forms.IntegerField(
                label = 'Max # of Assassinable Roles',
                initial = 3,
                widget = forms.NumberInput(
                    attrs={
                        'class':'form-text',
                        'min': '0',
                        'max': '3',
                 }))
    # delete so 'format' is not an actual field displayed
    del format
    
    def __init__(self, *args, **kwargs) -> None:
        super(GameForm, self).__init__(*args, **kwargs)
        self.roles = game_logic.ALL_ROLES
        # remove the colon from labels
        self.label_suffix = ""
        
    def roles(self) -> list:
        # print([field for field in self if 'percent' not in str(field)])
        return [field for field in self]# if 'percent' not in str(field)]
    
    def percents(self) -> list:
        return [field for field in self if 'percent' in str(field)]

    def get_fields(self) -> tuple:
        # print(zip(self.roles(), self.percents()))
        return zip(self.roles(), self.percents())
        
    def get_roles(self) -> tuple:
        return self.roles

    def clean(self) -> dict:
        super(GameForm, self).clean()
        cleaned_data = super(GameForm, self).clean()
        iseult = cleaned_data.get(game_logic.ISEULT)
        tristan = cleaned_data.get(game_logic.TRISTAN)
        if iseult != tristan:
            self.add_error(game_logic.ISEULT, "Both iseult and tristan must have the same likelyhood")
        if self.cleaned_data[game_logic.MIN_ASSASSIN] > self.cleaned_data[game_logic.MAX_ASSASSIN]:
            self.add_error(game_logic.MIN_ASSASSIN, "Min # of assassinable roles cannot be greater than max")
        return cleaned_data

class JoinExistingGame(forms.Form):
    game_id = forms.CharField(
                max_length=6,
                label="Game ID",
                error_messages={'invalid': "Invalid Game ID"},
                required=True,
                widget=forms.TextInput(
                    attrs={'class': 'form-control text-center',
                            'placeholder': 'Enter 6-character Game ID', 
                            'style': 'font-size:1rem;text-transform:uppercase;',
                            'autocomplete':'off'
                            }))
class ChangeName(forms.Form):
    first_name = forms.CharField(
                label="First Name",
                error_messages={'invalid': "Invalid Name"},
                widget=forms.TextInput(
                    attrs={
                        'class':'form-control',
                        'placeholder': 'First Name',
                        'style': 'font-size:1.25rem;'
                        }))
    last_name = forms.CharField(
                label="Last Name",
                error_messages={'invalid': "Invalid Name"},
                widget=forms.TextInput(
                    attrs={
                        'class':'form-control',
                        'placeholder': 'Last Name',
                        'style': 'font-size:1.25rem;'
                        }))