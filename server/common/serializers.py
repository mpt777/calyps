from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import TagType, Tag

from .models import *


class TagTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagType
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(), slug_field="model"
    )
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "tag_type", "content_type", "object_id", "content_object"]

    def get_content_object(self, obj):
        return str(obj.content_object) if obj.content_object else None

############################################################

class TagTypeActionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    DELETE = serializers.BooleanField(default=False)

    def validate_name(self, value):
        """Ensure the tag name is always lowercase."""
        return value.lower()
    

class TagAssignmentSerializer(serializers.Serializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(), slug_field="model"
    )
    object_id = serializers.IntegerField()
    tag_types = serializers.ListField(
        child=TagTypeActionSerializer()
    )

    def create(self, validated_data):
        content_type = validated_data["content_type"]
        object_id = validated_data["object_id"]
        tag_type_actions = validated_data["tag_types"]

        response_tags = []

        for action in tag_type_actions:
            tag_name = action["name"]
            delete_flag = action.get("DELETE", False)

            # Fetch or create the tag type
            tag_type, _ = TagType.objects.get_or_create(name=tag_name)

            if delete_flag:
                # If DELETE is True, try to remove the tag
                Tag.objects.filter(tag_type=tag_type, content_type=content_type, object_id=object_id).delete()
            else:
                # Otherwise, get or create the tag
                tag, _ = Tag.objects.get_or_create(
                    tag_type=tag_type,
                    content_type=content_type,
                    object_id=object_id,
                )
                response_tags.append(tag)

        return response_tags

    def to_representation(self, instance):
        return {
            "tags": [
                {"id": tag.id, "tag_type": tag.tag_type.name, "object_id": tag.object_id}
                for tag in instance
            ]
        }

##############################################################

class VisibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Visibility
        fields = ["id", "name", "code", "color", "sequence"]




        