from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todo/home.html')


# Create your views here.
def signupuser(request):
    """It handles signup user, checks if passwords do match if so it saves user to database and logins,
     if they dont or user exist,informs by returning error"""

    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:  # POST
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Username taken'})

        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':  # when user visits this page
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:  # POST, when user post data (fills form)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')
