from django.forms import ModelForm, Textarea
from django import forms
# from online.models import UserFunction
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class customAuthenticationForm(forms.Form):
    
    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']
        
class customLoginForm(AuthenticationForm):
    
    def __init__(self,*args, **kwargs):
        super(customLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password']