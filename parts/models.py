from django.db import models

# Create your models here.


class Part (models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.name + '--' + self.category
