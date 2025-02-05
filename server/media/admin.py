from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'file')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_by', 'image')
    raw_id_fields = ("uploaded_by",)

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
