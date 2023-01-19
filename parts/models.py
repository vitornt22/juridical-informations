# flake8: noqa
from django.db import models

from process.models import Process

# Create your models here.


class Part (models.Model):
    process = models.ManyToManyField(
        Process, related_name='parts', blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.name + '--' + self.category
