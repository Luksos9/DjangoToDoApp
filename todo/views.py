from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


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


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)  # by that we select todos by pk and only for user
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Wrong input'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
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


@login_required
def createtodo(request):
    if request.method == 'GET':  # when user visits this page
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:  # POST, when user post data (fills form)
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)  # Create but wait with saving
            newtodo.user = request.user  # now create when we specify user that creates todos
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': "Bad data passed in. Try again"})
