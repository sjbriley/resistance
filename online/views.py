from django.shortcuts import redirect, render
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from online.forms import customAuthenticationForm, customLoginForm

# Create your views here.

def home_page(request):
    form = customLoginForm()
    if request.method == 'POST':
        form = customLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = authenticate(username=username, password='')
            if user:
                login(request, user)
                return render(request, 'home.html', {'form':form})
            else:
                return render(request, 'home.html', {'form':form, 'userError':'User does not exist.'})
        else:
            print(form.errors)
    return render(request, 'home.html', {'form':form})

def online_new(request):
    return render(request, 'online_new.html')

def sign_up(request):
    form = customAuthenticationForm()
    if request.method == 'POST':
        form = customAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.create_user(username = username, password = '')
            user.is_active = True
            login(request, user)
            return redirect(reverse('home_page'))
        else:
            print(form.errors)
    return render(request, 'registration/sign_up.html', {'form':form})

def my_account(request):
    return render(request, 'my_account.html')