from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

import datetime

from .parse_restaurants import parse_amiga, parse_sodexo, parse_newton


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
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



def menu_page(request, week_day = str(datetime.datetime.now().isoweekday()) ):


    restaurants = []

    #return HttpResponse(parse_amiga(week_day))
    #return HttpResponse(parse_sodexo(week_day))
    #return HttpResponse(parse_newton(week_day))
    restaurants.append(parse_newton(week_day))
    restaurants.append(parse_sodexo(week_day))
    restaurants.append(parse_amiga(week_day))

    #data = "asd"
    #for item in data:
    #    data2 = item.get('MealOptions')


    return render(request, 'menu.html', {'restaurants': restaurants})
