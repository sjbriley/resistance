from django.forms import ModelForm, Textarea
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser, OnlineGames

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
        
    def clean_username(self):
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
    
    def __init__(self,*args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password']
    class Meta:
        model = CustomUser
        fields = ('username',)

# contains all fields in game setup
# add to the list as roles are added
FIELDS = [
            'jester_good', 'jester_good_percent', 
            'merlin_good', 'merlin_good_percent',
            'percival_good', 'percival_good_percent', 
            'uther_good', 'uther_good_percent',
            'tristan_good', 'tristan_good_percent',
            'iseult_good', 'iseult_good_percent',
            'arthur_good', 'arthur_good_percent',
            'lancelot_good', 'lancelot_good_percent',
            'guinevere_good', 'guinevere_good_percent',
            'mordred_bad', 'mordred_bad_percent',
            'morgana_bad', 'morgana_bad_percent',
            'maelagant_bad', 'maelagant_bad_percent',
            'colgrevance_bad', 'colgrevance_bad_percent',
            'assassin_bad', 'assassin_bad_percent'
        ]
class GameForm(forms.Form):
    
    # good roles
    jester_good      = forms.BooleanField(label="jester", required=False, initial=True)
    merlin_good      = forms.BooleanField(label="merlin", required=False, initial=True)
    percival_good    = forms.BooleanField(label="percival", required=False, initial=True)
    uther_good       = forms.BooleanField(label="uther", required=False, initial=True)
    tristan_good     = forms.BooleanField(label="tristan", required=False, initial=True)
    iseult_good      = forms.BooleanField(label="iseult", required=False, initial=True)
    arthur_good      = forms.BooleanField(label="arthur", required=False, initial=True)
    lancelot_good    = forms.BooleanField(label="lancelot", required=False, initial=True)
    guinevere_good   = forms.BooleanField(label="guinevere", required=False, initial=True)
    
    # bad roles
    mordred_bad     = forms.BooleanField(label="mordred", required=False, initial=True)
    morgana_bad     = forms.BooleanField(label="morgana", required=False, initial=True)
    maelagant_bad   = forms.BooleanField(label="maelagant", required=False, initial=True)
    colgrevance_bad = forms.BooleanField(label="colgrevance", required=False, initial=True)
    assassin_bad    = forms.BooleanField(label="assassin", required=False, initial=True)
    
    # define format to be used for percentage forms
    format = forms.IntegerField(
                initial = 100,
                widget = forms.NumberInput(
                    attrs={
                        'class':'form-text',
                        'min': '0',
                        'max': '100',
                 }))
    jester_good_percent = format
    merlin_good_percent = format
    percival_good_percent = format
    uther_good_percent = format
    tristan_good_percent = format
    iseult_good_percent = format
    arthur_good_percent = format
    lancelot_good_percent = format
    guinevere_good_percent = format
    mordred_bad_percent = format
    morgana_bad_percent = format
    maelagant_bad_percent = format
    colgrevance_bad_percent = format
    assassin_bad_percent = format
    # delete so 'format' is not an actual field displayed
    del format
    field_order = FIELDS

    def roles(self):
        # print([field for field in self if 'percent' not in str(field)])
        return [field for field in self if 'percent' not in str(field)]
    
    def percents(self):
        return [field for field in self if 'percent' in str(field)]

    def get_fields(self):
        # print(zip(self.roles(), self.percents()))
        return zip(self.roles(), self.percents())
        
    
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.roles = ('jester', 'merlin', 'percival', 'uther',
                      'tristan', 'iseult', 'arthur', 'lancelot',
                      'guinevere', 'mordred', 'morgana', 'maelagant',
                      'colgrevance', 'assassin')
        
    def getRoles(self):
        return self.roles
    class Meta:
        model = OnlineGames
        fields = FIELDS
        widgets = {}
        for role in fields:
            if 'percent' not in role:
                widgets[role] = forms.RadioSelect(
                    attrs={
                        'class': 'form-check-label',
                        'default': 'enabled'
                        })
        

    def clean(self):
        cleaned_data = super(GameForm, self).clean()
        iseult = cleaned_data.get("iseult")
        tristan = cleaned_data.get("tristan")
        iseult_good_percent = cleaned_data.get("iseult_good_percent")
        tristan_good_percent = cleaned_data.get("iseult_good_percent")
        if iseult != tristan:
            self.add_error('iseult', "Both iseult and tristan must be selected or not selected")
        if iseult_good_percent != tristan_good_percent:
            self.add_error('iseult', "Both iseult and tristan must have the same likelyhood")
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
    
    class Meta:
        model = OnlineGames
        fields = ('game_id',)
        
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