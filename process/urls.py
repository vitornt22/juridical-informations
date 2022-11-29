
# flake8: noqa
from django.urls import path

from parts import views as part_views

from . import views

app_name = 'process'

urlpatterns = [
    # urls clients
    path('home', views.Home.as_view(), name='home'),
    path('', views.LoginPage.as_view(), name='loginPage'),
    path('Logout', views.Logout.as_view(), name='logout'),
    path('detalhes/processo/<int:id>',
         views.ProcessClientsDetail.as_view(), name='detailClient'),
    path('pequisarProcessos/', views.ListingProcess.as_view(), name='searchProcess'),
    # urls adm
    path('processos', views.ProcessList.as_view(), name='list'),
    path('export', views.ProcessList.as_view(), name='export'),
    # register urls
    path('processo/registrar/', views.ProcessCreateView.as_view(), name='register'),
    path('processo/detalhes/<int:pk>/',
         views.ProcessUpdateView.as_view(), name='detail'),
    path('deletar/Processo/<int:pk>/',
         views.ProcessDeleteView.as_view(), name='delete'),
    path('desligarParte/<int:id>/<int:idPart>',
         views.ShutDownPart.as_view(), name='shutdown')

]
