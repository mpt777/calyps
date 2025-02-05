from django.contrib import admin
from django.db import models

from common.models import TimeStampedModel

# Register your models here.
CHOICES = (
  ("draft", "Draft"),
  ("private", "Private"),
  ("unlisted", "Unlisted"),
  ("friends", "Friends"),
  ("public", "Public"),
)

class Recipe(TimeStampedModel):
  name = models.CharField(max_length=255)
  handle = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  instructions = models.TextField(blank=True, null=True)
  
  image = models.ForeignKey("media.Image", related_name="recipies", blank=True, null=True, on_delete=models.SET_NULL)
  created_by = models.ForeignKey("auth.User", related_name="recipies", on_delete=models.CASCADE)

  prep_time = models.DurationField(blank=True, null=True)
  cook_time = models.DurationField(blank=True, null=True)

  servings = models.PositiveSmallIntegerField(default=1)

  visibility = models.CharField(default="draft", choices=CHOICES, max_length=255)

  def __str__(self):
    return self.name
