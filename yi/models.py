from django.db import models

# Create your models here.

class you_url(models.Model):
    url = models.CharField(max_length=10000)

