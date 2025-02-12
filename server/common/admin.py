from django.contrib import admin

from common.models import *


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tag_type", "content_type", "object_id", "content_object")
    list_filter = ("tag_type", "content_type")
    search_fields = ("name",)


@admin.register(Visibility)
class VisibilityAdmin(admin.ModelAdmin):
  list_display = ('name', 'code', 'color', 'sequence')
  search_fields = ("name", "code")


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "created_by")
    list_filter = ("created_by",)
    search_fields = ("name",)
    raw_id_fields = ("parent", "created_by")
