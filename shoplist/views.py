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

def parse_newton(week_day):

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

    got_url = url_base + '/' + get_kitchen + kitchenid + '&' + get_menuid + menu_id + '&' + week_part + week + '&' + which_weekday + week_day + '&' + which_language + language + '&' + which_format + wanted_format

    restaurant = dict()
    with urllib.request.urlopen(got_url) as food_url:
        s = food_url.read()
        s = s[1:-2]
        data = json.loads(s.decode('utf-8'))


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

    #return restaurant['meals'][0]["items"]
    return restaurant

def parse_sodexo(week_day):

    #"http://www.sodexo.fi/ruokalistat/output/daily_json/$kitchen/$timestr/fi"
    base = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'
    kitchenid = '12812'


    real_week_day = datetime.datetime.now().isoweekday()
    time_delta = datetime.timedelta(days=int(week_day) - int(real_week_day))

    timestamp = (datetime.datetime.today() + time_delta).strftime('%Y/%m/%d')

    got_url = base + kitchenid + "/" + timestamp + "/fi"

    restaurant = dict()
    with urllib.request.urlopen(got_url) as food_url:
        data = food_url.read()
        data = json.loads(data.decode('utf-8'))



    meals = []
    try:
        restaurant['name'] = data["meta"]["ref_title"]

        for c in data["courses"]:
            lunch = dict()

            item_in_meal = []
            lunch["name"] = c["title_en"]
            for ing in c["desc_en"].replace(" and", ",").split(", "):
                food = dict()
                food["name"] = ing
                if "properties" in c:
                    food["diets"] = c["properties"]

                item_in_meal.append(food)
            lunch["items"] = item_in_meal
            meals.append(lunch)
    except TypeError:
        restaurant['name'] = "TTY Tietotalo"

    restaurant['meals'] = meals

    if len(meals) == 0:
        restaurant['error'] = "No list for given day"

    # return restaurant['meals'][0]["items"]
    return restaurant

def parse_amiga(week_day):
    #http: // www.amica.fi / api / restaurant / menu / week?language = en & restaurantPageId = 69171 & weekDate =
    base = 'http://www.amica.fi/api/restaurant/menu/week?language=en&restaurantPageId=69171&weekDate='

    real_week_day = datetime.datetime.now().isoweekday()
    time_delta = datetime.timedelta(days=int(1) - int(real_week_day))

    timestamp = (datetime.datetime.today() + time_delta).strftime('%Y-%m-%d')
    got_url = base + timestamp
    restaurant = dict()
    with urllib.request.urlopen(got_url) as food_url:
        data = food_url.read()
        data = json.loads(data.decode('utf-8'))

    restaurant["name"] = "Amiga Reaktor"

    days_menu = []
    meals = []
    for day in data["LunchMenus"]:
        for set_menu in day["SetMenus"]:
            lunch = dict()

            item_in_meal = []
            lunch["name"] = set_menu["Name"]
            for ing in set_menu["Meals"]:
                food = dict()
                food["name"] = ing["Name"]
                food["diets"] = ing["Diets"]
                item_in_meal.append(food)
            lunch["items"] = item_in_meal
            meals.append(lunch)
        days_menu.append(meals)

    course = days_menu[int(week_day)-1]

    restaurant['meals'] = course

    if len(course) == 0:
        restaurant['error'] = "No list for given day"

    return restaurant

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
