# flake8: noqa
from django.db import models

from judge.models import Judge


class Process (models.Model):
    number = models.CharField(
        max_length=25, unique=True, null=True, blank=True)
    class_process = models.CharField(max_length=50, null=True, blank=True)
    court = models.CharField(max_length=50, null=True, blank=True)
    forum = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    organ = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    controll = models.CharField(max_length=50, null=True, blank=True)
    distribution = models.DateField(auto_now_add=True)
    judge = models.ForeignKey(
        Judge, on_delete=models.CASCADE, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)


# parts
# movement
