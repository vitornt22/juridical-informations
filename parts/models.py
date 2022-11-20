# flake8: noqa
from django.db import models

from process.models import Process

CATEGORIES = (('R', 'RÉU'), ('J', 'JUIZ'), ('A', 'AUTOR'))

# Create your models here.


class Part (models.Model):
    process = models.ManyToManyField(
        Process, related_name='parts')
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    category = models.CharField(choices=CATEGORIES, max_length=1)

    def __str__(self):
        return self.name + '--' + str(self.id)
