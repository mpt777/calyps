from django.db import models


class Entity(models.Model):
  name = models.CharField(max_length=255)
  code = models.CharField(max_length=255, unique=True)
  description = models.TextField(blank=True, null=True)

  class Meta:
    ordering = ("name",)

  def __str__(self) -> str:
    return self.name


# Create your models here.
class Configuration(models.Model):
  entity = models.ForeignKey(Entity, related_name="configurations", on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  data = models.JSONField(blank=True, null=True, default=dict)

  class Meta:
    ordering = ("entity", "name")

  def __str__(self) -> str:
    return self.name