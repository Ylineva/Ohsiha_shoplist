from django.db import models
from django.contrib.auth.models import User


class Shoplist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

# Create your models here.
class Ingredient(models.Model):

    amount_choices = (
        ('pc', 'pick'),
        ('kg', 'kilogram'),
        ('l', 'litre'),
        ('bag', 'bag'),
    )
    shoplist = models.ForeignKey(Shoplist, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    amount = models.CharField(max_length=3, choices=amount_choices)
    number_of_items = models.PositiveIntegerField()

    def __str__(self):
        return str(self.number_of_items) + ' ' + str(self.amount) + ' ' + str(self.name)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
