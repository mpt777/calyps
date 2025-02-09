from django.contrib.auth.models import Group, User
from rest_framework import routers, serializers, viewsets, permissions
from django.urls import include, path, re_path
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all().order_by('name')
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]



class SecretSantaRow(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SecretSantaRow
        fields = ['name']


class SecretSantaSerializer(serializers.HyperlinkedModelSerializer):
    rows = SecretSantaRow(many=True, read_only=True)

    class Meta:
        model = SecretSanta
        fields = ['name', "rows", "pairs_str"]




class SecretSantaViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = SecretSanta.objects.all()
    serializer_class = SecretSantaSerializer



router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

router.register(r'secret_santa', SecretSantaViewset)
urlpatterns = [
    path('', include(router.urls)),
]