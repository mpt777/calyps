from rest_framework import serializers
from .models import Recipe, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.SlugRelatedField(read_only=True, slug_field='code')  # Returns the unit as a string

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "recipe"]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)  # Nested ingredients
    image = serializers.StringRelatedField()  # Returns image as a string
    created_by = serializers.StringRelatedField()  # Returns username of creator
    visibility = serializers.SlugRelatedField(read_only=True, slug_field='code') # Returns visibility as a string

    class Meta:
        model = Recipe
        fields = [
            "id", "name", "handle", "description", "instructions",
            "image", "created_by", "prep_time", "cook_time",
            "servings", "visibility", "ingredients"
        ]
