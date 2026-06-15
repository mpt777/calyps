from django.contrib import admin

from iot.models import Entity, Configuration

# Register your models here.
@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

  
@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "entity")
