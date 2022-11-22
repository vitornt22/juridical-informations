from django.contrib import admin

from .models import Movement


# Register your models here.
@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    ...
