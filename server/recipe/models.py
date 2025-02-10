import bleach
from django.contrib import admin
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify

from common.models import TimeStampedModel

# Register your models here.

BLEACH = {
  "tags": ["b", "i", "strong", "em", "p", "ul", "ol", "li", "a", "span", "div", "h1","h2","h3","h4","h5","h6", "blockquote", "s","u"] ,
  "attributes": {"a": ["href"], "span":["contenteditable"], "*": ["class", "data-list"]},
  "protocols": ["http", "https"] 
}

class Recipe(TimeStampedModel):
  name = models.CharField(max_length=255)
  handle = models.CharField(max_length=255, unique=True)
  description = models.TextField(blank=True, null=True)
  instructions = models.TextField(blank=True, null=True)
  
  image = models.ForeignKey("media.Image", related_name="recipies", blank=True, null=True, on_delete=models.SET_NULL)
  created_by = models.ForeignKey("auth.User", related_name="recipies", on_delete=models.CASCADE)

  prep_time = models.PositiveIntegerField(blank=True, null=True)
  cook_time = models.PositiveIntegerField(blank=True, null=True)

  servings = models.PositiveSmallIntegerField(default=1)

  # visibility = models.CharField(default="draft", choices=CHOICES, max_length=255)
  visibility = models.ForeignKey("common.Visibility", related_name="recipes", on_delete=models.PROTECT)

  def __str__(self):
    return self.name
  
  def clean(self):
    self.handle = slugify(self.handle)
    if self.handle in ["add", "edit"]:
      raise ValidationError({"handle":"Invalid Handle"})
  
  def save(self, *args, **kwargs):
    self.handle = slugify(self.handle)
    if self.description:
     self.description = bleach.clean(self.description, **BLEACH)
    if self.instructions:
      self.instructions = bleach.clean(self.instructions, **BLEACH)

    super(Recipe, self).save(*args, **kwargs)
    


class Ingredient(TimeStampedModel):
  recipe = models.ForeignKey("Recipe", related_name="ingredients", on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  amount = models.FloatField(default=1.0)
  unit = models.ForeignKey("Unit", related_name="ingredients", on_delete=models.PROTECT)
  sequence = models.PositiveSmallIntegerField(default=0)

  class Meta:
    ordering = ("recipe", "sequence")

  def __str__(self):
    return self.name
  


SYSTEM_CHOICES = (
  (0, "Imperial"),
  (1, "Metric")
)

KIND_CHOICES = (
  (0, "Volume"),
  (1, "Weight")
)

class Unit(models.Model):
  name = models.CharField(max_length=255)
  code = models.CharField(max_length=6)
  system = models.PositiveSmallIntegerField(choices=SYSTEM_CHOICES)
  kind = models.PositiveSmallIntegerField(choices=KIND_CHOICES)

  def __str__(self):
    return f"{self.name} {self.code}"