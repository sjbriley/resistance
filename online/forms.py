from django.forms import ModelForm, Textarea
from django import forms
# from online.models import UserFunction
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from online.models import CustomUser

class customAuthenticationForm(forms.Form):
    
    username = forms.CharField(max_length=30,
                                label="Username",
                                error_messages={'invalid': "Invalid Username"})
    
    # def __init__(self,*args, **kwargs):
        # super(customAuthenticationForm, self).__init__(*args, **kwargs)
        # self.password1 = 'password'
        # self.fields['password2'].initial = 'password'
        # self.fields['password2'].initial = 'password'
        # del self.fields['password2']
    
    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("A user with that username already exists.")
        else:
            return self.cleaned_data['username']
        
    def save(self, commit=True):
        user = super(customAuthenticationForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
    
    def clean(self):            
        return self.cleaned_data
    
    
    class Meta:
        model = CustomUser
        fields = ('username',)
        widgets = {
            'username': Textarea(attrs={
                'placeholder': 'Enter Username',
                'class': 'form-control',
            })}
        
class customLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30,
                                label="Username",
                                error_messages={'invalid': "Invalid Username"})
    
    def __init__(self,*args, **kwargs):
        super(customLoginForm, self).__init__(*args, **kwargs)
        del self.fields['password']
    # def clean(self):
    #     pass
    # def is_valid(self):
    #     super(customLoginForm, self).is_valid()
    #     if User.objects.filter(username__iexact=self.cleaned_data['username']):
    #         return True
    #     else:
    #         raise ValidationError