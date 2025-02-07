from rest_framework import serializers

from .models import *

class VisibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Visibility
        fields = ["id", "name", "code", "color", "sequence"]