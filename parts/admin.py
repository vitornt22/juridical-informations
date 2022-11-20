from django.contrib import admin

from .models import Part


# Register your models here.
@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    ...
