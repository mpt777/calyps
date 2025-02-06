from django.forms import ValidationError


class DataInitializer:

  def __init__(self, data, model, unique):
    self.data = data
    self.model = model
    self.unique = unique
  
  def process(self):
    for data in self.data:
      found = self.model.objects.filter(**{self.unique: data[self.unique]})
      found_count = found.count()
      if found_count == 0:
        self.model.objects.get_or_create(**data)
      elif found_count == 1:
        found.update(**data)
      else:
        raise ValidationError("Too many instances returned!")
      



class DataInitializerRegister:
  def __init__(self):
    self.instances = []

  def process(self):
    for data in self.instances:
      data.process()

  def register(self, instance):
    self.instances.append(instance)


data_register = DataInitializerRegister()
