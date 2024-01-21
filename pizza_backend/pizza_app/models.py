from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class Ingredient(models.Model):
    CATEGORY_CHOICES = (
        ('basico', 'Basico'),
        ('premium', 'Premium'),
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES, default='basic')

class User(AbstractUser):
    USER_TYPES = (
        ('normal', 'Normal'),
        ('staff', 'Staff'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')

class Pizza(models.Model):
    STATE_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    name = models.CharField(max_length=100)
    price = models.IntegerField(validators=[MinValueValidator(0)],)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='active')
    ingredients = models.ManyToManyField(Ingredient)
