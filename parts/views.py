from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import PartForm
from .models import Part


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class PartUpdateView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'adm/parts/partDetail.html'
    success_url = 'part:detail'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_process'] = self.kwargs.get('id_process')
        # flake8
        context['path'] = 'process:detail' if context['id_process'] \
            is not None else 'part:list'
        return context

    def form_valid(self, form):
        part = form.save(commit=False)
        part.save()
        messages.success(self.request, 'Parte registrada com sucess')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        id_process = self.kwargs.get('id_process')
        pk = self.kwargs.get('pk')

        if id_process is None:
            return redirect('part:list')
        else:
            return redirect('part:processDetailEditPart',
                            id_process=id_process, pk=pk)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class PartCreateView(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:register'

    def form_valid(self, form):
        part = form.save(commit=False)
        part.save()
        messages.success(self.request, 'Parte registrada com sucess')

    def post(self, request, * args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.request.path == '/processo/partes/registrar/':
            return redirect('process:register')
        elif 'processo/detalhes/' in self.request.path:
            id = self.kwargs.get('id')
            return redirect('process:detail', id)
        else:
            return redirect('part:list')


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class PartDeleteView(View):
    # specify the model you want to use
    def get(self, request, pk=None, * args, **kwargs):
        part = Part.objects.filter(id=pk).first()
        if part:
            messages.success(request, 'Parte deletada com sucesso')
            part.delete()
        else:
            messages.error(request, 'Erro ao tentar deletar')
            raise Http404()
        return redirect('part:list')


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
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
                Q(category__icontains=search)
            ))

        return qs

    def get_context_data(self, *args, **kwargs):
        part_form = PartForm()
        ctx = super().get_context_data(*args, **kwargs)
        ctx['partPath'] = 'part:register'
        ctx.update({"active": 2, 'tag': 'Parto',
                   'path': 'list', 'part_form': part_form})
        return ctx
