# flake8: noqa
from django.db import models


class Process (models.Model):
    number = models.CharField(
        max_length=25, unique=True, null=True, blank=True)
    class_project = models.CharField(max_length=50)
    court = models.CharField(max_length=50)
    forum = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    organ = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    controll = models.CharField(max_length=50, null=True, blank=True)
    distribution = models.DateField(auto_now_add=True)
    value = models.FloatField()
    status = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    # parts
    # movement
