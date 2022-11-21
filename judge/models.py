from django.db import models


# Create your models here.
class Judge(models.Model):
    name = models.CharField(max_length=100, null=False)
    cnj = models.CharField(max_length=18, null=False, )

    def __str__(self) -> str:
        return self.name + " - " + self.cnj
