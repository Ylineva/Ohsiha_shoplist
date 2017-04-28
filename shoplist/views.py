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

    if len(Shoplist.objects.filter(user=request.user)) == 0:
        shoplist = Shoplist.objects.create(user=request.user)
    else:
        shoplist = Shoplist.objects.filter(user=request.user)[0]

    ingredients = Ingredient.objects.filter(shoplist=shoplist)
    shop_list = []

    for i in range(len(ingredients)):
        shop_list.append(ingredients[i])

    return render(request, 'home.html', {'user': request.user, 'shop_list': shop_list})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():

            user = User.objects.create_user(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])

            student = Student.objects.create(user=user)

            return HttpResponseRedirect('/')

    return render(request, 'registration/register.html', {'form': form})



def menu_page(request, week_day = str(datetime.datetime.now().isoweekday()) ):


    restaurants = []

    restaurants.append(parse_newton(week_day))
    restaurants.append(parse_sodexo(week_day))
    restaurants.append(parse_amiga(week_day))

    return render(request, 'menu.html', {'restaurants': restaurants})
