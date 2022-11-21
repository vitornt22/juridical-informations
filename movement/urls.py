
# flake8: noqa
from django.urls import path

from . import views

app_name = 'movement'
urlpatterns = [
    path('RegistrarMovimentacao/<int:id>/',
         views.MovementDetails.as_view(), name='register'),
    path('Editar/Movimentacao/<int:idProcess>/<int:id>/',
         views.MovementDetails.as_view(), name='detail'),
    path('movement/deletar/<int:id>/',
         views.MovementDelete.as_view(), name='delete')
]
