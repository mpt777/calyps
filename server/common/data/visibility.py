from common.models import Visibility
from server.data.initialize import DataInitializer, data_register 


data = [
  {"name": "Draft", "code": "draft", "sequence": 0},
  {"name": "Private", "code": "private","sequence": 1},
  {"name": "Unlisted", "code": "unlisted","sequence": 2},
  {"name": "Friends", "code": "friends", "sequence": 3},
  {"name": "Public", "code": "public", "sequence": 4},
]

data_register.register(DataInitializer(data, Visibility, "code"))