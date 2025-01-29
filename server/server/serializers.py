
from django import forms
from django.contrib.auth.models import Group, User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(label='Password', write_only=True)
    password2 = serializers.CharField(label='Password confirmation', write_only=True)

    def validate(self, data):
        print(data)
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ( "id", "username", "email", "password1", "password2")


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value
    
# from django import forms
# from django.contrib.auth.models import Group, User
# from rest_framework import routers, serializers, viewsets, permissions
# from django.urls import include, path, re_path


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
