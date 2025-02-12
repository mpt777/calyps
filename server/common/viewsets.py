from django.urls import include, path
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from utils.view.utils import check_owner_permission
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.routers import DefaultRouter
from rest_framework.views import exception_handler

from .models import *
from .serializers import *


class TagTypeViewSet(viewsets.ModelViewSet):
    queryset = TagType.objects.all()
    serializer_class = TagTypeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class VisibilityViewset(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer

router = DefaultRouter()
router.register(r'visibility', VisibilityViewset, basename='visibility')
router.register(r'tag-type', TagTypeViewSet, basename='tagtype')
router.register(r'tag', TagViewSet, basename='tag')


class TagAssignmentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TagAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            tags = serializer.save()
            return Response(serializer.to_representation(tags), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Include the router's URLs into your URL configuration
urlpatterns = [
    path('', include(router.urls)),  # Prefix the API endpoints with "api/"
    path('tag-assign', TagAssignmentView.as_view(), name="tag-assign"),
]