from django.forms import ModelForm, Textarea
from django import forms
# from online.models import UserFunction
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from online.models import GameLog, CustomUser

roles = ()

class CustomAuthenticationForm(forms.Form):

    username = forms.CharField(
                                max_length=30,
                                label="Username",
                                error_messages={'invalid': "Invalid Username"},
                                widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your unique username'}),
                                )
    
    def clean_username(self):
        existing = CustomUser.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']
    class Meta:
        model = CustomUser
        fields = ('username',)
        
class CustomLoginForm(AuthenticationForm):
    
    username = forms.CharField(
                                max_length=30,
                                label="Username",
                                error_messages={'invalid': "Invalid Username"},
                                widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Choose a unique username'}),
                                )
    
    def __init__(self,*args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password']
    class Meta:
        model = CustomUser
        fields = ('username',)

class GameForm(forms.Form):
    
    # good roles
    jester = forms.BooleanField(label="jester", required=False, initial=True)
    merlin = forms.BooleanField(label="merlin", required=False, initial=True)
    percival = forms.BooleanField(label="percival", required=False, initial=True)
    uther = forms.BooleanField(label="uther", required=False, initial=True)
    tristan = forms.BooleanField(label="tristan", required=False, initial=True)
    iseult = forms.BooleanField(label="iseult", required=False, initial=True)
    arthur = forms.BooleanField(label="arthur", required=False, initial=True)
    lancelot = forms.BooleanField(label="lancelot", required=False, initial=True)
    guinevere = forms.BooleanField(label="guinevere", required=False, initial=True)
    
    # bad roles
    mordred = forms.BooleanField(label="mordred", required=False, initial=True)
    morgana = forms.BooleanField(label="morgana", required=False, initial=True)
    maelagant = forms.BooleanField(label="maelagant", required=False, initial=True)
    colgrevance = forms.BooleanField(label="colgrevance", required=False, initial=True)
    assassin = forms.BooleanField(label="assassin", required=False, initial=True)
    
    
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.roles = ('jester', 'merlin', 'percival', 'uther', 'tristan', 'iseult', 'arthur', 'lancelot', 'guinevere',
                    'mordred', 'morgana', 'maelagant', 'colgrevance', 'assassin')
        
    def getRoles(self):
        return self.roles
    class Meta:
        model = GameLog
        fields = ['__all__']
        widgets = {}
        good = ('jester', 'merlin')
        for role in fields:
            widgets[role] = forms.RadioSelect(attrs={'class': 'form-check-label', 'default': 'enabled'})

    def clean(self):
        cleaned_data = super(GameForm, self).clean()
        iseult = cleaned_data.get("iseult")
        tristan = cleaned_data.get("tristan")
        if iseult != tristan:
            self.add_error('iseult', "Both iseult and tristan must be selected or not selected")
        return cleaned_data
class JoinExistingGame(forms.Form):
    gameID = forms.CharField(
                                max_length=6,
                                label="Game ID",
                                error_messages={'invalid': "Invalid Game ID"},
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Enter 6-character Game ID', 'style': 'font-size:1.25rem;text-transform:uppercase;'})
                            )
    
    class Meta:
        model = GameLog