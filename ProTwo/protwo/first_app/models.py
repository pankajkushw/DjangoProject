from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id = models.EmailField()

    def __str__(self):
        return self.first_name
    def __str__(self):
        return self.last_name
