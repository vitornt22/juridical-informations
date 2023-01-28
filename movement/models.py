from django.db import models

from process.models import Process


# Create your models here.
class Movement(models.Model):
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=500)
    process = models.ForeignKey(
        Process, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id) + " - "
