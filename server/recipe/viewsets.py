from django.urls import include, path
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Recipe, Ingredient, Unit
from .serializers import RecipeSerializer, IngredientSerializer, UnitSerializer
from utils.view.utils import check_owner_permission
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.routers import DefaultRouter
from rest_framework.views import exception_handler

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)  # Raises ValidationError if invalid
            recipe = serializer.save()

            # Custom success response
            return Response(
                {"message": "Recipe created successfully!", "recipe": RecipeSerializer(recipe).data},
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            # Custom error response
            return Response(
                {"message": "Validation failed", "errors": e.detail},  # e.detail contains the error dictionary
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @check_owner_permission()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)  # Supports both PUT (full update) and PATCH (partial update)
        instance = self.get_object()  # Get the existing object
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            updated_recipe = serializer.save()

            # Custom success response
            return Response(
                {"message": "Recipe updated successfully!", "recipe": RecipeSerializer(updated_recipe).data},
                status=status.HTTP_200_OK
            )

        except ValidationError as e:
            # Custom error response
            return Response(
                {"message": "Update failed", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
    
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


class UnitViewset(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


router = DefaultRouter()
router.register(r'recipe', RecipeViewSet, basename='recipe')
router.register(r'ingredient', IngredientViewSet, basename='ingredient')
router.register(r'unit', UnitViewset, basename='unit')

# Include the router's URLs into your URL configuration
urlpatterns = [
    path('', include(router.urls)),  # Prefix the API endpoints with "api/"
]