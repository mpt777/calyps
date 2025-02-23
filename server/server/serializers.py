
from django import forms
from django.contrib.auth.models import Group, User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(label='Password', write_only=True)
    password1 = serializers.CharField(label='Password confirmation', write_only=True)

    def validate(self, data):
        if data['password1'] != data['password']:
            raise serializers.ValidationError({"password1": "Passwords do not match."})
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({"username": "Username is taken"})
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already has an account associated with it"})
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
        fields = ( "id", "username", "email", "password1", "password")


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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', "date_joined", "last_login"]
