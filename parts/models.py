from django.db import models

from process.models import Process

CATEGORIES = (('R', 'RÉU'), ('J', 'JUIZ'), ('A', 'AUTOR'))


# Create your models here.
class Part (models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    category = models.CharField(choices=CATEGORIES, max_length=1)
