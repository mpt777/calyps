from django.urls import include, path
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Recipe, Ingredient, Unit
from .serializers import RecipeSerializer, IngredientSerializer, UnitSerializer
from utils.view.utils import check_owner_permission, require_authentication
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView, exception_handler
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.pagination import CursorPagination, PageNumberPagination


class RecipeAPIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, recipe_id=""):
        """Retrieve a recipe by ID or handle."""
        recipe_id = self.kwargs.get("pk")
        if not recipe_id:
            raise NotFound("Recipe not found. Provide either ID or handle.")
        
        try:
            return Recipe.objects.get(handle=recipe_id)
        except Recipe.DoesNotExist:
            try:
                return Recipe.objects.get(id=recipe_id)
            except (Recipe.DoesNotExist, ValueError):
                raise NotFound(f"Recipe with ID or handle {recipe_id} not found.")

    def get(self, request, *args, **kwargs):
        """Handle GET request to retrieve a specific recipe."""
        recipe_id = kwargs.get('pk')

        # if not recipe_id:
        #     recipes = Recipe.objects.all()
        #     serializer = RecipeSerializer(recipes, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)

        recipe = self.get_object(recipe_id)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @require_authentication
    def post(self, request, *args, **kwargs):
        """Handle POST request to create a new recipe."""
        serializer = RecipeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            recipe = serializer.save(created_by=request.user)  # Assuming user is set during creation
            return Response(
                {"message": "Recipe created successfully!", "recipe": RecipeSerializer(recipe).data},
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {"message": "Validation failed", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

    @check_owner_permission()
    def patch(self, request, *args, **kwargs):
        """Handle PATCH request to partially update an existing recipe."""
        recipe_id = kwargs.get('pk')
        print(kwargs)
        recipe = self.get_object(recipe_id)
        serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        
        try:
            serializer.is_valid(raise_exception=True)
            updated_recipe = serializer.save()
            return Response(
                {"message": "Recipe updated successfully!", "recipe": RecipeSerializer(updated_recipe).data},
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"message": "Update failed", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

    @check_owner_permission
    def delete(self, request, *args, **kwargs):
        """Handle DELETE request to delete a recipe."""
        recipe_id = kwargs.get('pk')
        recipe = self.get_object(recipe_id)

        if recipe.created_by != request.user:  # Check ownership
            return Response(
                {"message": "You do not have permission to delete this recipe."},
                status=status.HTTP_403_FORBIDDEN
            )

        recipe.delete()
        return Response(
            {"message": "Recipe deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100


class RecipeSearchView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RecipeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description', 'ingredients__name', "tags__tag_type__name"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Always apply hard filters before returning data.
        """
        ## Paginator
        return Recipe.objects.filter(
            Q(visibility__code="public") |
            Q(created_by_id=self.request.user.id)
            # Q(visibility__code__in=["friends"])
        ).distinct()
    
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     paginated_queryset = self.paginate_queryset(queryset)  # Automatically applies pagination

    #     if paginated_queryset is not None:
    #         serializer = self.get_serializer(paginated_queryset, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    @require_authentication
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
# router.register(r'recipe', RecipeViewSet, basename='recipe')
# router.register(r'recipe-search', RecipeSearchView, basename='recipe-search')
router.register(r'ingredient', IngredientViewSet, basename='ingredient')
router.register(r'unit', UnitViewset, basename='unit')

# Include the router's URLs into your URL configuration
urlpatterns = [
    path('', include(router.urls)),  # Prefix the API endpoints with "api/"
    path('search/recipe/', RecipeSearchView.as_view(), name='recipe-search'), 
    path('recipe/', RecipeAPIView.as_view(), name='recipe-list'), 
    path('recipe/<str:pk>/', RecipeAPIView.as_view(), name='recipe'), 
]