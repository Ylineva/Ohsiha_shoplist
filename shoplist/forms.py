from django import forms

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
