# flake8: noqa
from django.db import models

from process.models import Process

CATEGORIES = (('Réu', 'RÉU'), ('Juiz', 'JUIZ'), ('Autor', 'AUTOR'))

# Create your models here.


class Part (models.Model):
    process = models.ManyToManyField(
        Process, related_name='parts', blank=True)
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    category = models.CharField(choices=CATEGORIES, max_length=5)

    def __str__(self):
        return self.name + '--' + str(self.id)
