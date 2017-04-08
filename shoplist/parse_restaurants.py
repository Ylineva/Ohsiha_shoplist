import datetime
import urllib.request
import json

NEWTON_BASE_URL = 'http://www.juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx'
NEWTON_JSON = lambda x,y: NEWTON_BASE_URL + '/GetMenuByWeekday?KitchenId=6&MenuTypeId=60&Week=' + x + "&Weekday=" + y + "&lang='en'&format=json"

REAKTOR_BASE_URL = 'http://www.amica.fi/'
REAKTOR_JSON = lambda x: REAKTOR_BASE_URL + 'api/restaurant/menu/week?language=en&restaurantPageId=69171&weekDate=' + x

SODEXO_BASE_URL = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'
SODEXO_JSON = lambda x: SODEXO_BASE_URL + '12812/' + x + "/fi"


def parse_newton(week_day):

    week = str(datetime.datetime.now().isocalendar()[1])
    got_url = NEWTON_JSON(week, week_day)

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

    return restaurant



def parse_sodexo(week_day):

    real_week_day = datetime.datetime.now().isoweekday()
    time_delta = datetime.timedelta(days=int(week_day) - int(real_week_day))

    timestamp = (datetime.datetime.today() + time_delta).strftime('%Y/%m/%d')

    got_url = SODEXO_JSON(timestamp)
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

    return restaurant


def parse_amiga(week_day):

    real_week_day = datetime.datetime.now().isoweekday()
    time_delta = datetime.timedelta(days=int(1) - int(real_week_day))

    timestamp = (datetime.datetime.today() + time_delta).strftime('%Y-%m-%d')

    got_url = REAKTOR_JSON(timestamp)
    restaurant = dict()
    with urllib.request.urlopen(got_url) as food_url:
        data = food_url.read()
        data = json.loads(data.decode('utf-8'))

    restaurant["name"] = "Amiga Reaktor"

    days_menu = []

    for day in data["LunchMenus"]:
        meals = []
        for set_menu in day["SetMenus"]:
            lunch = dict()

            item_in_meal = []
            lunch["name"] = set_menu["Name"]
            for ing in set_menu["Meals"]:
                food = dict()
                food["name"] = ing["Name"]
                food["diets"] = ", ".join(ing["Diets"])
                item_in_meal.append(food)
            lunch["items"] = item_in_meal
            meals.append(lunch)
        days_menu.append(meals)

    course = days_menu[int(week_day)-1]

    restaurant['meals'] = course

    if len(course) == 0:
        restaurant['error'] = "No list for given day"
    return restaurant
