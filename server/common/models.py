from django.db import models
from django.forms import ValidationError

from server.fields import ColorField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#Django model utils TimeStampedModel
class TimeStampedModel(models.Model):
  """
  An abstract base class model that provides self-updating
  ``created`` and ``modified`` fields.

  """
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      abstract = True



class Visibility(models.Model):
  name = models.CharField(max_length=255)
  code = models.CharField(max_length=15)
  color = ColorField(default="#777")
  sequence = models.PositiveSmallIntegerField(default=0)

  class Meta:
    ordering = ("sequence",)

  def __str__(self):
    return f"{self.name} {self.code}"


class TagType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_type = models.ForeignKey("TagType", related_name="tags", on_delete=models.CASCADE)

    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, related_name="tags", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
       unique_together = ("tag_type", "content_type", "object_id")

    def __str__(self):
        return self.tag_type.name

    def clean(self):
       self.name = self.name.lower()


class Collection(models.Model):
  name = models.CharField(max_length=255)
  parent = models.ForeignKey("Collection", related_name="children", blank=True, null=True, on_delete=models.SET_NULL)
  created_by = models.ForeignKey("auth.User", related_name="collections", on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.name}"
  
  def clean(self):
    if self.parent:
       if self.parent.created_by != self.created_by:
          raise ValidationError("Parent was not created by the same person")