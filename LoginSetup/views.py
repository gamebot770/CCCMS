# Create your views here.
#views.py
from LoginSetup.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, redirect

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables,)

def register_success(request):
    return render_to_response('registration/welcome.html',{'user': request.user} )

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            home(request)
        else:
            # Return a 'disabled account' error message
            return render_to_response('login.html', {'user': request.user})
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect('/register/')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    return render_to_response('registration/welcome.html', {'user': request.user})
