from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


def delete(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(Ingredient, pk=pk)
        item.delete()

    return HttpResponseRedirect('/add/')

@login_required
def edit_page(request, pk):

    if request.method == 'POST':
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



@login_required
def list_view(request):

    if len(Shoplist.objects.filter(user=request.user)) == 0:
        shoplist = Shoplist.objects.create(user=request.user)
    else:
        shoplist = Shoplist.objects.filter(user=request.user)[0]

    if request.method == 'POST':

        form = IngredientForm(request.POST)
        if form.is_valid():

            ingredient = Ingredient.objects.create(name=form.cleaned_data['name'],
                                                   amount=form.cleaned_data['amount'],
                                                   number_of_items=form.cleaned_data['number_of_items'],
                                                   shoplist=shoplist)

            return HttpResponseRedirect('/add/')

    else:
        form = IngredientForm()

    ingredients = Ingredient.objects.filter(shoplist=shoplist)
    shop_list = []

    for i in range(len(ingredients)):
        shop_list.append(ingredients[i])

    return render(request, 'add_view.html', {'form': form, 'shop_list': shop_list})
