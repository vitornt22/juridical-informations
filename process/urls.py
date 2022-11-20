
# flake8: noqa
from django.urls import path

from . import views

app_name = 'process'
urlpatterns = [
    path('', views.ProcessList.as_view(), name='list'),
    path('processo/', views.ProcessDetails.as_view(), name='register'),
    path('processo/<int:id>/', views.ProcessDetails.as_view(), name='detail'),
    path('a/<int:id>/', views.ProcessDelete.as_view(), name='delete')
]
