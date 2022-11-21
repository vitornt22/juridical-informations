# flake8: noqa
from django.db import models

from judge.models import Judge


class Process (models.Model):
    number = models.CharField(
        max_length=25, unique=True, null=True, blank=True)
    class_process = models.CharField(max_length=50)
    court = models.CharField(max_length=50)
    forum = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    organ = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    controll = models.CharField(max_length=50, null=True, blank=True)
    distribution = models.DateField(auto_now_add=True)
    judge = models.ForeignKey(
        Judge, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.FloatField()
    status = models.BooleanField(default=True, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

# parts
# movement
