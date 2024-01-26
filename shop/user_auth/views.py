from django.shortcuts import render, redirect
from .forms import NewUserForm , UpdateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, User
# Create your views here.

def user_register(request):
    if request.method == "POST":
        register_form = NewUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('main:index')
    register_form = NewUserForm()
    return render(request=request, template_name='user_auth/register.html', context={'register_form': register_form})


def user_login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login( request, user)
                return redirect('main:index')
    login_form = AuthenticationForm()
    return render(request=request, template_name='user_auth/login.html', context={'login_form': login_form})

def user_cab(request):
    print(User.objects.all())
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
    return render(request, 'user_auth/cab.html')

def user_logout(request):
    logout(request)
    return redirect('main:index')

def user_change(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('main:index')
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'user_auth/change_profile.html',{'user_form': user_form})


        