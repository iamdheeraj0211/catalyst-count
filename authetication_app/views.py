from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.models import User


def signupview(request):

    form = UserCreationForm()
    template_name = 'auth/signup.html'
    context = {'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account created Successfully! ')
            return redirect('login_url')
        else:
            messages.error(request, 'Please enter details in given format')
    return render(request, template_name, context)


def loginview(request):
    template_name = 'auth/login.html'
    context = {}
    if request.user != 'AnonymousUser':
        logout(request)
    if request.method == 'POST':
        u = request.POST.get('un')
        p = request.POST.get('pw')

        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            request.session['username'] = u

            messages.success(request, 'You have logged in Successfully ')
            return redirect('addorder_url')
        else:
            messages.error(request, 'Please enter correct details')
    return render(request, template_name, context)


def logoutview(request):
    request.session.flush()
    logout(request)
    messages.error(request, 'You have been logged out!')
    return redirect('login_url')


def loginview1(request):
    form = AuthenticationForm()
    template_name = 'auth/login.html'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            messages.success(request, 'You have logged in Successfully ')
            return redirect('addorder_url')
        else:
            messages.error(request, 'Please enter correct details')
    context = {'form': form}
    return render(request, template_name, context)


def formView(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'show_url', {"username": username})
    else:
        return render(request, 'auth/login.html', {})



@login_required(login_url='login_url')
def showorfileview(request):
    if request.session.has_key("username"):
        data = User.objects.all()
        template_name = 'auth/show_user.html'
        context = {'obj': data}
        return render(request, template_name, {'obj': data, "udata": request.session["username"]})
    else:
        return redirect("login_url")
    