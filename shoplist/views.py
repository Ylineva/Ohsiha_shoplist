from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('home/')
    else:
        return login(request)

@login_required
def home_page(request):
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")

    return render_to_response(
        'home.html',
        {'user': request.user}
    )


def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():

            student = Student.objects.create(user=User.objects.create(username=form.cleaned_data['username'],
                                                   password=form.cleaned_data['password1']))

            return HttpResponseRedirect('/')

    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

