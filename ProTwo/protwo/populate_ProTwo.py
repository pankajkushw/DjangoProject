import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protwo.settings')

import django
django.setup


import random
from first_app.models import Person
from faker import Faker

fakegen = Faker()
