from django.urls import include, path
from rest_framework import viewsets
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from utils.view.utils import check_owner_permission
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.routers import DefaultRouter

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_object(self):
        recipe_id = self.kwargs.get('pk')  # `pk` corresponds to the recipe ID

        if not recipe_id:
            raise NotFound("Recipe not found. Provide either ID or handle.")
        
        try:
            return Recipe.objects.get(handle=recipe_id)
        except Recipe.DoesNotExist:
            try:
                return Recipe.objects.get(id=recipe_id)
            except Recipe.DoesNotExist:
                raise NotFound(f"Recipe with ID or handle {recipe_id} not found.")

    def perform_create(self, serializer):
        """Automatically assign created_by during recipe creation."""
        serializer.save(created_by=self.request.user)

    @check_owner_permission()
    def update(self, request, *args, **kwargs):
        """Update a recipe (only if the current user is the creator)."""
        return super().update(request, *args, **kwargs)

    @check_owner_permission()
    def destroy(self, request, *args, **kwargs):
        """Delete a recipe (only if the current user is the creator)."""
        return super().destroy(request, *args, **kwargs)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        """Automatically assign the recipe to the ingredient during creation."""
        recipe = serializer.validated_data.get('recipe')
        if recipe.created_by != self.request.user:
            raise PermissionDenied("You cannot add ingredients to this recipe.")
        serializer.save()

    @check_owner_permission(obj_attr='recipe__created_by')
    def update(self, request, *args, **kwargs):
        """Update an ingredient (only if the current user is the creator of the recipe)."""
        return super().update(request, *args, **kwargs)

    @check_owner_permission(obj_attr='recipe__created_by')
    def destroy(self, request, *args, **kwargs):
        """Delete an ingredient (only if the current user is the creator of the recipe)."""
        return super().destroy(request, *args, **kwargs)


router = DefaultRouter()
router.register(r'recipe', RecipeViewSet, basename='recipe')
router.register(r'ingredient', IngredientViewSet, basename='ingredient')

# Include the router's URLs into your URL configuration
urlpatterns = [
    path('', include(router.urls)),  # Prefix the API endpoints with "api/"
]