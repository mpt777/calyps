from django.urls import include, path
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Visibility
from .serializers import VisibilitySerializer
from utils.view.utils import check_owner_permission
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.routers import DefaultRouter
from rest_framework.views import exception_handler


class VisibilityViewset(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer

router = DefaultRouter()
router.register(r'visibility', VisibilityViewset, basename='visibility')

# Include the router's URLs into your URL configuration
urlpatterns = [
    path('', include(router.urls)),  # Prefix the API endpoints with "api/"
]