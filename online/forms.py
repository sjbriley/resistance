from django.forms import ModelForm, Textarea
from django import forms
# from online.models import UserFunction
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from online.models import GameLog, CustomUser

class customAuthenticationForm(forms.Form):

    username = forms.CharField(max_length=30,
                                label="Username",
                                error_messages={'invalid': "Invalid Username"})
    
    def clean_username(self):
        existing = CustomUser.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']
    class Meta:
        model = CustomUser
        fields = ('username',)
        
class customLoginForm(AuthenticationForm):
    
    def __init__(self,*args, **kwargs):
        super(customLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password']
    class Meta:
        model = CustomUser
        fields = ('username',)

class GameForm(forms.Form):
    
    class Meta:
        model = GameLog
        fields = ['__all__']
        widgets = {
            'jester': forms.RadioSelect(),
            'merlin': forms.RadioSelect(),
            'assasin': forms.RadioSelect(),
            'puck': forms.RadioSelect(),
        } 