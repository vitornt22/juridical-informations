
# flake8: noqa
from django.urls import path

from . import views

app_name = 'part'
urlpatterns = [
    path('partes/', views.PartList.as_view(), name='list'),
    path('parte/', views.PartDetails.as_view(), name='register'),
    path('<str:path>/novaParte/', views.PartDetails.as_view(), name='register'),
    path('parte/<int:id>/', views.PartDetails.as_view(), name='detail'),
    path('a/<int:id>/', views.PartDelete.as_view(), name='delete')
]
