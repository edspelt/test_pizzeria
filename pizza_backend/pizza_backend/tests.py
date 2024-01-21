
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from pizza_app.models import Pizza, Ingredient
from rest_framework.authtoken.models import Token

User = get_user_model()

class PizzaAPITestCase(APITestCase):
    def setUp(self):
        # Crear usuario staff con permisos adecuados
        self.user_staff = User.objects.create_user(username='staff', password='staff123', is_staff=True, user_type='staff')
        self.staff_token = Token.objects.create(user=self.user_staff)

        # Autenticar al cliente de test con el token del usuario staff
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)

        # Crear ingredientes de prueba
        self.ingredient1 = Ingredient.objects.create(name='Tomate', category='basico')
        self.ingredient2 = Ingredient.objects.create(name='Queso', category='basico')

        # Crear pizza de prueba
        self.pizza = Pizza.objects.create(name='Margherita', price=10000, state='activo')
        self.pizza.ingredients.add(self.ingredient1, self.ingredient2)

    def test_create_pizza(self):
        data = {
            'name': 'Pepperoni', 
            'price': 100000, 
            'state': 'activo', 
            'ingredients': [self.ingredient1.id, self.ingredient2.id] 
        }
        response = self.client.post(reverse('pizzas'), data)
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_pizzas(self):
        response = self.client.get(reverse('pizzas'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pizza_ingredient_association(self):
        response = self.client.post(reverse('pizza-ingredient-association', kwargs={'pizza_id': self.pizza.id, 'ingredient_id': self.ingredient2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('pizza-ingredient-association', kwargs={'pizza_id': self.pizza.id, 'ingredient_id': self.ingredient2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
