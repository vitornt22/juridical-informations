# flake8: noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from judge.forms import JudgeForm
from judge.models import Judge
from parts.forms import PartForm
from parts.models import Part
from process.forms import ProcessForm


class PartUpdateView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'adm/parts/partDetail.html'
    success_url = 'part:detail'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['idP'] = self.kwargs.get('idP')
        context['path'] = 'process:detail' if context['idP'] is not None else 'part:list'
        return context

    def form_valid(self, form):
        part = form.save(commit=False)
        part.save()
        messages.success(self.request, 'Parte registrada com sucess')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        idP = self.kwargs.get('idP')
        pk = self.kwargs.get('pk')

        if idP is None:
            print("IP= NONE")
            return redirect('part:list')
        else:
            print('entra aqui')
            return redirect('part:processDetailEditPart', idP=idP, pk=pk)


class PartCreateView(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:register'

    def form_valid(self, form):
        part = form.save(commit=False)
        part.save()
        messages.success(self.request, 'Parte registrada com sucess')

    def form_invalid(self, form):
        part = form.data['cpf']
        if Part.objects.filter(cpf=part).exists():
            messages.error(self.request, 'CNJ existente, tente novamente')
        else:
            messages.error(self.request, 'Erro ao tentar registrar')

    def post(self, request, * args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.request.path == '/processo/partes/registrar/':
            return redirect('process:register')
        elif 'processo/detalhes/' in self.request.path:
            id = self.kwargs.get('id')
            return redirect('process:detail', id)
        else:
            return redirect('part:list')


class PartDeleteView(View):
    # specify the model you want to use
    def get(self, request, pk=None, * args, **kwargs):
        part = Part.objects.filter(id=pk).first()
        if part:
            messages.success(request, 'Parte deletada com sucesso')
            part.delete()
        else:
            messages.error(request, 'Erro ao tentar deletar')
            return redirect('process:detail', pk)


class PartListView(ListView):
    model = Part
    context_object_name = 'parts'
    ordering = ['-id']
    template_name = 'adm/parts/partsList.html'

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)

        if search:
            qs = qs.filter(Q(
                Q(name__icontains=search) |
                Q(category__icontains=search) |
                Q(cpf__icontains=search)
            ))

        return qs

    def get_context_data(self, *args, **kwargs):
        partForm = PartForm()
        ctx = super().get_context_data(*args, **kwargs)
        ctx['partPath'] = 'part:register'
        ctx.update({"active": 2, 'tag': 'Parto',
                   'path': 'list', 'partForm': partForm})
        return ctx
