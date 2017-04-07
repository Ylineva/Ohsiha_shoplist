from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
import urllib.request
import json

import datetime



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


    url_to_fetch = "http://www.juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?KitchenId=$kitchen&MenuTypeId=$menutype&Week=$week&Weekday=$weekday&lang='fi'&format=json";
    url_base = 'http://www.juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx'
    kitchenid = '6'
    get_kitchen = 'GetMenuByWeekday?KitchenId='
    menu_id = '60'
    get_menuid = 'MenuTypeId='
    week = str(datetime.datetime.now().isocalendar()[1])
    week_part = 'Week='
    which_weekday = "Weekday="
    which_language = "lang="
    language = "'en'"
    which_format = "format="
    wanted_format = "json"

    path_to_name = ['d', 'KitchenName']
    path_to_food = ['d', 'MealOptions']

    got_url = url_base + '/' + get_kitchen + kitchenid + '&' + get_menuid + menu_id + '&' + week_part + week + '&' + which_weekday + week_day + '&' + which_language + language + '&' + which_format + wanted_format

    restaurant = dict()
    with urllib.request.urlopen(got_url) as food_url:
        s = food_url.read()
        s = s[1:-2]

        data = json.loads(s.decode('utf-8'))

    restaurants = []
    data = data['d']
    data = json.loads(data)
    restaurant['name'] = data['KitchenName']
    data = data['MealOptions']
    meals = []
    lunch_name = []

    foods = []

    for m in data:
        item_in_menu = []
        for meal in m["MenuItems"]:
            item_in_menu.append(meal)
        foods.append(item_in_menu)
        lunch_name.append(m["Name_EN"])


    for i in range(len(foods)):
        f = foods[i]
        lunch = dict()
        item_in_meal = []

        for m in f:
            food = dict()
            if len(m["Name_EN"]) == 0:
                continue
            food["name"] = m["Name_EN"]
            food["diets"] = m["Diets"]
            item_in_meal.append(food)
        lunch["name"] = lunch_name[i]
        lunch["items"] = item_in_meal
        meals.append(lunch)

    restaurant['meals'] = meals

    if len(meals) == 0:
        restaurant['error'] = "No list for given day"


    restaurants.append(restaurant)

    #data = "asd"
    #for item in data:
    #    data2 = item.get('MealOptions')

    message = {'msg': restaurants}
    return render(request, 'menu.html', {'restaurants': restaurants})
