from django.contrib import admin

from recipe.models import *

# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
  list_display = ('name', 'handle', 'created_by')
  raw_id_fields = ("created_by", "image")

admin.site.register(Recipe, RecipeAdmin)