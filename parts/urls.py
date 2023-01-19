
# flake8: noqa
from django.urls import path

from . import views

app_name = 'part'
urlpatterns = [
    path('partes/', views.PartListView.as_view(), name='list'),
    # edit urls
    path('editarParte/<int:pk>/', views.PartUpdateView.as_view(), name='detail'),
    path('process/<int:idP>/editarParte/<int:pk>/',
         views.PartUpdateView.as_view(), name="processDetailEditPart"),
    # register urls
    path('partes/novaParte/',
         views.PartCreateView.as_view(), name='register'),
    path('processo/detalhes/<int:id>/registrarParte/',
         views.PartCreateView.as_view(), name='processDetailPart'),
    path('processo/partes/registrar/',
         views.PartCreateView.as_view(), name='processPartRegister'),
    # delete urls
    path('deletar/<int:pk>/', views.PartDeleteView.as_view(), name='delete'),

]
