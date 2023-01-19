# Create your views here.
# flake8: noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from process.forms import ProcessForm

from .forms import JudgeForm
from .models import Judge


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeUpdateView(UpdateView):
    model = Judge
    form_class = JudgeForm
    template_name = 'adm/judge/judgeDetail.html'
    success_url = 'judge:detail'

    def form_invalid(self, form):
        messages.success(self.request, 'Dados Editados')

    def form_valid(self, form):
        judge = form.save(commit=False)
        judge.save()
        id = self.kwargs.get('pk')
        messages.success(self.request, 'Dados Editados')
        return redirect('judge:detail', id)


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeCreateView(CreateView):
    model = Judge
    form_class = JudgeForm
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:list'

    def form_invalid(self, form):
        messages.error(self.request, 'Erro, tente novamente')

    def form_valid(self, form):
        judge = form.save(commit=False)
        if Judge.objects.filter(cnj=judge.cnj).exists():
            messages.error(self.request, 'CNJ existente, tente novamente')
        else:
            judge.save()
            messages.success(self.request, 'Juiz registrada com sucess')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if request.path == '/processo/juiz/registrar':
            return redirect('process:register')
        elif 'processo/detalhes/' in request.path:
            id = kwargs.get('id')
            return redirect('process:detail', id)
        else:
            return redirect('judge:list')


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeDeleteView(View):
    # specify the model you want to use
    def get(self, request, *args, **kwargs):
        judge = Judge.objects.filter(id=kwargs.get('pk')).first()
        if judge:
            messages.success(request, 'Juiz deletado com sucesso')
            judge.delete()
        else:
            messages.error(request, 'Erro ao tentar deletar')
            raise Http404()
        return redirect('judge:list')


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeList(ListView):
    model = Judge
    context_object_name = 'judges'
    ordering = ['-id']
    template_name = 'adm/judge/judgesList.html'

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)
        if search is not None:
            qs = qs.filter(Q(
                Q(name__icontains=search) |
                Q(cnj__icontains=search))
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        judgeForm = JudgeForm()
        ctx = super().get_context_data(*args, **kwargs)
        ctx['judgePath'] = 'judge:RegisterJudge'
        ctx.update({"active": 3, 'tag': 'Juiz',
                   'judgeForm': judgeForm, 'path': 'list'})
        return ctx
