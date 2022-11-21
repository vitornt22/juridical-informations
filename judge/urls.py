
# flake8: noqa
from django.urls import path

from . import views

app_name = 'judge'
urlpatterns = [
    path('juizes/', views.JudgeList.as_view(), name='list'),
    path('<str:path>/novo/juiz/', views.JudgeDetails.as_view(), name='register'),
    path('Editar/juiz/<int:id>/', views.JudgeDetails.as_view(), name='detail'),
    path('judge/deletar/<int:id>/', views.JudgeDelete.as_view(), name='delete')
]
