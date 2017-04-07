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


def delete(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(Ingredient, pk=pk)
        item.delete()

    return HttpResponseRedirect('/add/')

def edit_page(request, pk):

    if request.method == 'POST':
        #return HttpResponse("asd")
        form = IngredientForm(request.POST)
        if form.is_valid():
            item = get_object_or_404(Ingredient, pk=pk)
            item.name = form.cleaned_data['name']
            item.amount = form.cleaned_data['amount']
            item.number_of_items = form.cleaned_data['number_of_items']
            item.save()
            return HttpResponseRedirect('/add/')

    item = get_object_or_404(Ingredient, pk=pk)

    ingr = {
        'name': item.name,
        'amount': item.amount,
        'number_of_items': item.number_of_items,
    }

    form = IngredientForm(ingr)

    return render(request, 'edit_view.html', {'form': form, 'pk': pk})


def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():

            student = Student.objects.create(user=User.objects.create(username=form.cleaned_data['username'],
                                                   password=form.cleaned_data['password1'])
                                             )

            return HttpResponseRedirect('/')

    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def list_view(request):
    if request.method == 'POST':

        form = IngredientForm(request.POST)
        if form.is_valid():

            ingredient = Ingredient.objects.create(name=form.cleaned_data['name'],
                                                   amount=form.cleaned_data['amount'],
                                                   number_of_items=form.cleaned_data['number_of_items'])

            return HttpResponseRedirect('/add/')

    else:
        form = IngredientForm()

    ingredients = Ingredient.objects.all()
    shop_list = []

    for i in range(len(ingredients)):
        shop_list.append(ingredients[i])


    return render(request, 'add_view.html', {'form': form, 'shop_list': shop_list})
