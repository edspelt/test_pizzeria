from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView,
    PizzaListCreateView,
    PizzaDetailView,
    IngredientListCreateView,
    IngredientDetailView,
    PizzaIngredientAssociationView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pizzas/', PizzaListCreateView.as_view(), name='pizzas'),
    path('pizzas/<int:pk>/', PizzaDetailView.as_view(), name='pizza-detail'),
    path('pizza_ingredientes/<int:pizza_id>/ingredient/<int:ingredient_id>/', PizzaIngredientAssociationView.as_view(), name='pizza-ingredient-association'),
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredients'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
]