
# flake8: noqa
from django.urls import path

from . import views

app_name = 'process'
urlpatterns = [
    path('', views.ProcessList.as_view(), name='processList'),
]
