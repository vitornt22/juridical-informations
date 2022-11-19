# flake8: noqa
from django.db import models


class Process (models.Model):
    number = models.CharField(
        max_length=25, unique=True, null=False, blank=False)
    class_project = models.CharField(max_length=50)
    court = models.CharField(max_length=50)
    forum = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    organ = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    distribution = models.DateField(auto_now_add=True)
    value = models.FloatField()
    slug = models.SlugField()
    # parts
    # movement
