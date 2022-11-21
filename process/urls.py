
# flake8: noqa
from django.urls import path

from parts import views as part_views

from . import views

app_name = 'process'
urlpatterns = [
    path('', views.ProcessList.as_view(), name='list'),
    path('processo/', views.ProcessDetails.as_view(), name='register'),
    path('processo/<int:id>/', views.ProcessDetails.as_view(), name='detail'),
    path('deletarProcesso/<int:id>/',
         views.ProcessDelete.as_view(), name='delete'),
    path('desligarParte/<int:id>/<int:idPart>',
         views.DeleteProcessPart.as_view(), name='shutdown')

]
