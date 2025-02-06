from django.contrib import admin

from common.models import *


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class VisibilityAdmin(admin.ModelAdmin):
  list_display = ('name', 'code', 'color', 'sequence')
  search_fields = ("name", "code")


admin.site.register(Visibility, VisibilityAdmin)
admin.site.register(Tag, TagAdmin)