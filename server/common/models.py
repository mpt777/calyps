from django.db import models

from server.fields import ColorField

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


class Tag(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name