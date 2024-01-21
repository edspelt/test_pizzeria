from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Pizza, Ingredient
from .serializers import UserSerializer, PizzaSerializer, IngredientSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

User = get_user_model()

class StaffPermission(permissions.BasePermission):
    """Permiso personalizado para permitir solo a usuarios de tipo 'staff'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'staff'

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)

class PizzaListCreateView(generics.ListCreateAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pizza.objects.all()
        return Pizza.objects.filter(state='activo')

class PizzaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [permissions.IsAuthenticated, StaffPermission]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(serializer.data)  
        return Response({"message": "El ingrediente se actualizo correctamentey"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "El ingrediente se elimino correctamente"}, status=status.HTTP_200_OK)

class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated, StaffPermission]

class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated, StaffPermission]

class PizzaIngredientAssociationView(APIView):
    permission_classes = [permissions.IsAuthenticated, StaffPermission]

    def post(self, request, pizza_id, ingredient_id):
        try:
            pizza = Pizza.objects.get(pk=pizza_id)
            ingredient = Ingredient.objects.get(pk=ingredient_id)
        except (Pizza.DoesNotExist, Ingredient.DoesNotExist):
            return Response({"error": "Pizza o Ingrediente no existe"}, status=status.HTTP_404_NOT_FOUND)

        pizza.ingredients.add(ingredient)
        pizza.save()

        return Response({"message": "Se asocio correctamente el ingrediente"}, status=status.HTTP_200_OK)

    def delete(self, request, pizza_id, ingredient_id):
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

        if ingredient in pizza.ingredients.all():
            pizza.ingredients.remove(ingredient)
            pizza.save()
            return Response({"message": "Los ingredientes se eliminaron correctamente de la pizza"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "El ingrediente no esta asociado a la pizza"}, status=status.HTTP_400_BAD_REQUEST)
