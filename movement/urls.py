
# flake8: noqa
from django.urls import path

from . import views

app_name = 'movement'
urlpatterns = [
    path('registrarMovimentacao/<int:idProcess>/',
         views.MovementCreateView.as_view(), name='register'),
    path('editar/Movimentacao/<int:idProcess>/<int:pk>/',
         views.MovementUpdateView.as_view(), name='detail'),
    path('movimentacao/deletar/<int:pk>/',
         views.MovementDeleteView.as_view(), name='delete')
]
