from recipe.models import Unit
from server.data.initialize import DataInitializer

from server.data.initialize import data_register

data = [
  {"name": "cup", "code": "cup", "system": 0, "kind": 0},
  {"name": "teaspoon", "code": "tsp", "system": 0, "kind": 0},
  {"name": "tablespoon", "code": "tbsp", "system": 0, "kind": 0},
  {"name": "pint", "code": "pt", "system": 0, "kind": 0},
  {"name": "quart", "code": "qt", "system": 0, "kind": 0},
  {"name": "gallon", "code": "gal", "system": 0, "kind": 0},
  {"name": "ounce", "code": "oz", "system": 0, "kind": 1},
  {"name": "fluid ounce", "code": "fl oz", "system": 0, "kind": 0},
  {"name": "pound", "code": "lb", "system": 0, "kind": 1},
  {"name": "milliliter", "code": "ml", "system": 1, "kind": 0},
  {"name": "liter", "code": "l", "system": 1, "kind": 0},
  {"name": "gram", "code": "g", "system": 1, "kind": 1},
  {"name": "kilogram", "code": "kg", "system": 1, "kind": 1}
]

data_register.register(DataInitializer(data, Unit, "code"))
