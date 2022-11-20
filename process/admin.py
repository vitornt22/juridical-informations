from django.contrib import admin

from .models import Process

# Register your models here.


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    ...
