# flake8: noqa
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from process.models import Process

from .admin_processes_views import ProcessDelete, ProcessDetails, ProcessList


class Home(View):
    def get(self, request):
        return render(request, 'clients/index.html', {'active': "1"})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('process:loginPage')


class LoginPage(View):
    def get(self, request):
        return render(request, 'adm/loginPage.html', {})

    def post(self, request, *args, **kwargs):
        print('ENTROU AQUI')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print("USUARIO", user)
            return redirect(reverse('process:list'))
        else:
            messages.error(
                request, "Senha ou email Invalidos, tente novamente !")
        return redirect('process:loginPage')


class ProcessClientsDetail(View):
    def get(self, request, id=None):
        process = Process.objects.filter(id=id).first()
        return render(request, 'clients/details.html', {'process': process, 'active': 2})


class ListingProcess(ListView):
    model = Process
    context_object_name = 'processes'
    ordering = ['-distribution']
    template_name = 'clients/processesSearched.html'

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)
        if search:
            qs = qs.filter(Q(
                Q(number__icontains=search) |
                Q(court__icontains=search) | Q(forum__icontains=search) |
                Q(judge__name__icontains=search) | Q(class_process__icontains=search) |
                Q(subject__icontains=search) | Q(organ__icontains=search) |
                Q(area__icontains=search) | Q(county__icontains=search)
            ))

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'active': 2})
        return ctx
