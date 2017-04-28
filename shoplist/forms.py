from django import forms
from .models import *
import re

class IngredientForm(forms.Form):
    amount_choices = (
        ('pc', 'pick'),
        ('kg', 'kilogram'),
        ('l', 'litre'),
        ('bag', 'bag'),
    )

    name = forms.CharField(label="Ingredient", max_length=60)
    number_of_items = forms.IntegerField(label="Amount")
    amount = forms.ChoiceField(label="", widget=forms.RadioSelect(), choices=amount_choices)

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=60)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput())

    # method is called when form.is_valid() is run
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # fetch forms cleaned data
        password = cleaned_data['password1']
        password2 = cleaned_data['password2']
        username = cleaned_data['username']

        errors = []
        # Error if password do not match
        if password != password2:
            errors.append(forms.ValidationError('Passwords do not match.'))
        # Error if other than alphanumeric characters or underscore is used in username
        if not re.search(r'^\w+$', username):
            errors.append(forms.ValidationError('Username can only contain alphanumeric characters and the underscore.'))
        # Error if user with given name exists already
        if len(User.objects.filter(username=username)) != 0:
            errors.append(forms.ValidationError('Username is already taken.'))

        if len(errors) != 0:
            raise forms.ValidationError(errors)

        return cleaned_data