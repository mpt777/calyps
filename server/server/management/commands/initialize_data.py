from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from server.data.initialize import data_register

class Command(BaseCommand):

  def handle(self, *args, **options):
    print(data_register.instances)
    data_register.process()