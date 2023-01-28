
from django.urls import path

from . import views

app_name = 'movement'
urlpatterns = [
    path('registrarMovimentacao/<int:id_process>/',
         views.MovementCreateView.as_view(), name='register'),
    path('editar/Movimentacao/<int:id_process>/<int:pk>/',
         views.MovementUpdateView.as_view(), name='detail'),
    path('movimentacao/deletar/<int:pk>/',
         views.MovementDeleteView.as_view(), name='delete')
]
