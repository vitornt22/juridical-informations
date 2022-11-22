
# flake8: noqa
from django.urls import path

from . import views

app_name = 'part'
urlpatterns = [
    path('partes/', views.PartList.as_view(), name='list'),
    path('<str:path>/novaParte/',
         views.PartDetails.as_view(), name='register'),
    path('editarParte/<int:id>/', views.PartDetails.as_view(), name='detail'),
    path('editarParte/<int:id>/<int:idP>/',
         views.PartDetails.as_view(), name='detailPartProcess'),
    path('deletar/<int:id>/', views.PartDelete.as_view(), name='delete')
]
