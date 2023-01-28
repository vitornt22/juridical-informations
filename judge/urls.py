
from django.urls import path

from . import views

app_name = 'judge'
urlpatterns = [
    path('juizes/', views.JudgeList.as_view(), name='list'),
    path('juiz/Editar/<int:pk>/',
         views.JudgeUpdateView.as_view(), name='detail'),
    # register urls
    path('juiz/registrarJuiz',
         views.JudgeCreateView.as_view(), name='RegisterJudge'),
    path('processo/juiz/registrar', views.JudgeCreateView.as_view(),
         name='registerProcessJudge'),
    path('processo/detalhes/<int:id>/registrarJuiz',
         views.JudgeCreateView.as_view(), name='processDetailJudge'),
    # delete urls
    path('juiz/deletar/<int:pk>/',
         views.JudgeDeleteView.as_view(), name='delete')
]
