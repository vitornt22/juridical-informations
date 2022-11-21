
# flake8: noqa
from django.urls import path

from parts import views as part_views

from . import views

app_name = 'process'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('Login', views.LoginPage.as_view(), name='loginPage'),
    path('Logout', views.Logout.as_view(), name='logout'),
    path('detalhes/processo/<int:id>',
         views.ProcessClientsDetail.as_view(), name='detailClient'),
    path('pequisarProcessos/', views.ListingProcess.as_view(), name='searchProcess'),
    path('processos', views.ProcessList.as_view(), name='list'),
    path('processo/', views.ProcessDetails.as_view(), name='register'),
    path('processo/<int:id>/', views.ProcessDetails.as_view(), name='detail'),
    path('deletar/Processo/<int:id>/',
         views.ProcessDelete.as_view(), name='delete'),
    path('desligarParte/<int:id>/<int:idPart>',
         views.DeleteProcessPart.as_view(), name='shutdown')

]
