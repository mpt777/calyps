from django.contrib import admin

from common.models import *

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Tag, TagAdmin)