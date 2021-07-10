from django.shortcuts import render

# Create your views here.
def home_local(request):
    return render(request, 'local/new_local.html')