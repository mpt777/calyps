from rest_framework import serializers
from .models import Recipe, Ingredient, Unit
from django.contrib.auth.models import User

class IngredientSerializer(serializers.ModelSerializer):
    unit_code = serializers.SlugRelatedField(read_only=True, slug_field='code', source='unit')  # Returns the unit as a string

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "recipe"]

class IngredientInlineSerializer(IngredientSerializer):
    DELETE = serializers.BooleanField(default=False)

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "recipe", "DELETE"]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInlineSerializer(many=True)
    image = serializers.StringRelatedField()  # Returns image as a string
    created_by = serializers.StringRelatedField()  # Returns username of creator
    # visibility = serializers.SlugRelatedField(queryset=Visibility., slug_field='code') # Returns visibility as a string

    class Meta:
        model = Recipe
        fields = [
            "id", "name", "handle", "description", "instructions",
            "image", "created_by", "prep_time", "cook_time",
            "servings", "visibility", "ingredients"
        ]

    def _process_related(self, instance, ingredients_data):
      for ingredient_data in ingredients_data:
        DELETE = ingredient_data.pop("DELETE", False)
        ID = ingredient_data.pop("id", None)

        if DELETE and ID:
            Ingredient.objects.filter(id=ID).delete()
            continue
        if ID:
            ingredient = Ingredient.objects.get(id=ID)
            for attr, value in ingredient_data.items():
                setattr(ingredient, attr, value)
        else:
            ingredient = Ingredient.objects.create(**ingredient_data)
            instance.ingredients.add(ingredient)
            
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        validated_data["created_by"] = User.objects.get(id=1)
        recipe = Recipe.objects.create(**validated_data)
        self._process_related(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')

        for i in range(len(ingredients_data)):
            ingredients_data[i]["id"] = self.initial_data["ingredients"][i]["id"]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._process_related(instance, ingredients_data)
        return instance
