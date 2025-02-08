from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from server import views

urlpatterns = [
    path("", views.index),
    path("files/", include('media.urls')),
    path("admin/", admin.site.urls),
    path('api/v1/social/', include('social.api')),
    path('api/v1/auth/', include('server.api')),
    path('api/v1/recipe/', include('recipe.viewsets')),
    path('api/v1/common/', include('common.viewsets')),
    # path('api/v1/auth/', include('server.api')),


]

if bool(settings.DEBUG):
    urlpatterns += static(f"{settings.MEDIA_URL}", document_root=f"{settings.MEDIA_ROOT}")