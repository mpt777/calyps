from rest_framework import serializers

from common.serializers import VisibilitySerializer
from common.models import Visibility

from .models import Recipe, Ingredient, Unit
from django.contrib.auth.models import User


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name", "code", "system", "kind"]


class IngredientSerializer(serializers.ModelSerializer):
    unit_code = serializers.SlugRelatedField(read_only=True, slug_field='code', source='unit')  # Returns the unit as a string

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "recipe"]

class IngredientInlineSerializer(IngredientSerializer):
    DELETE = serializers.BooleanField(default=False)
    # _id = serializers.IntegerField()

    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance',"")
    #     if instance:
    #         kwargs['initial'] = kwargs.get('initial', {})
    #         kwargs['initial']['form_id'] = instance.id 

    #     super().__init__(*args, **kwargs)

    

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "unit_code","sequence", "DELETE"]
        # extra_kwargs = {
        #     '_id': {'write_only': True},
        # }


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInlineSerializer(many=True, required=False, allow_empty=True)
    image = serializers.StringRelatedField()  # Returns image as a string
    created_by = serializers.StringRelatedField()  # Returns username of creator
    # visibility = serializers.SlugRelatedField(queryset=Visibility., slug_field='code') # Returns visibility as a string
    # visibility_choices = serializers.SerializerMethodField()
    # unit_choices = serializers.SerializerMethodField()
    # prep_time = serializers.SerializerMethodField()
    # cook_time = serializers.SerializerMethodField()

    # def get_prep_time(self, obj):
    #     print(obj.prep_time.total_seconds())
    #     return obj.prep_time.total_seconds() if obj.prep_time else 0

    # def get_cook_time(self, obj):
    #     print(obj.cook_time.total_seconds())
    #     return obj.cook_time.total_seconds() if obj.cook_time else 0

    def get_visibility_choices(self, obj):
        return VisibilitySerializer(Visibility.objects.all(), many=True).data
    
    def get_unit_choices(self, obj):
        return UnitSerializer(Unit.objects.all(), many=True).data


    class Meta:
        model = Recipe
        fields = [
            "id", "name", "handle", "description", "instructions",
            "image", "created_by", "prep_time", "cook_time",
            "servings", "visibility", "ingredients",
            # "visibility_choices", "unit_choices"
        ]

    def _process_related(self, instance, ingredients_data):
      for ingredient_data in ingredients_data:
        DELETE = ingredient_data.pop("DELETE", False)
        ID = ingredient_data.pop("id", None)

        if DELETE:
            if ID:
                Ingredient.objects.filter(id=ID).delete()
                continue
            continue
        if ID:
            ingredient = Ingredient.objects.get(id=ID)
            for attr, value in ingredient_data.items():
                setattr(ingredient, attr, value)
                ingredient.save()
        else:
            ingredient_data["recipe"] = instance
            ingredient = Ingredient.objects.create(**ingredient_data)
            instance.ingredients.add(ingredient)
            
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        validated_data["created_by"] = User.objects.get(id=1)
        recipe = Recipe.objects.create(**validated_data)
        self._process_related(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])

        for i in range(len(ingredients_data)):
            ingredients_data[i]["id"] = self.initial_data["ingredients"][i].get("id", "")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._process_related(instance, ingredients_data)
        return instance
