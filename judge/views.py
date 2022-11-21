# Create your views here.
# flake8: noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.list import ListView

from .forms import JudgeForm
from .models import Judge


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeDetails(View):

    def render_judge(self, form, html, id, idP):
        print('entra aqui')
        return render(self.request, html, context={'form': form,
                                                   'active': 3, 'tag': 'Projeto',
                                                   'back': 'judge:list',
                                                   'id': id})

    def get_judge(self, id=None):
        judge = None
        if id is not None:
            judge = Judge.objects.filter(
                pk=id
            ).first()

            if not judge:
                raise Http404()
        return judge

    def get(self, request, id=None):
        print("diiiiidiidi", id)
        html = 'adm/process/processRegister.html' if id is None else 'adm/judge/judgeDetail.html'
        judge = self.get_judge(id)

        form = JudgeForm(instance=judge or None)
        return self.render_judge(form, html, id)

    def post(self, request, id=None, path=None):
        judge = self.get_judge(id)
        print('entrando POST')
        form = JudgeForm(request.POST, request.FILES, instance=judge)
        print("IDDD", id)

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            # now i can make changes in object edited
            p.save()
            if id is not None:
                messages.success(
                    request, 'Juiz  Editado  com sucesso!')
            else:
                messages.success(
                    request, 'Juiz Cadastrado com sucesso!')
        else:
            print('no')

        if id is None:
            if path == 'processo':
                return redirect('process:register')
            elif 'editar' in path:
                idProcess = int(path.replace('editar', ''))
                print('myInt', idProcess)
                return redirect('process:detail', idProcess)
            else:
                return redirect('part:list')

        print('chegando ate aqui')
        html = 'adm/judge/judgeDetail.html'

        return self.render_judge(form, html, id)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeDelete(JudgeDetails):
    def get(self, request, id=None):
        print("DELETEEE")
        judge = Judge.objects.filter(id=id).first()
        name = judge.name
        judge.delete()
        messages.success(self.request, name+'(a) Deletado com sucesso')
        return redirect('judge:list')


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeList(ListView):
    model = Judge
    context_object_name = 'judges'
    ordering = ['-id']
    template_name = 'adm/judge/judgesList.html'

    def get_queryset(self, *args, **kwargs):
        print('HELLO')
        search = self.request.GET.get('search')
        print(search)
        qs = super().get_queryset(*args, **kwargs)
        if search is not None:
            print('akoosjdojo')
            qs = qs.filter(Q(Q(name__icontains=search)
                           | Q(cnj__icontains=search)))
        return qs

    def get_context_data(self, *args, **kwargs):
        judgeForm = JudgeForm()
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 3, 'tag': 'Juiz',
                   'judgeForm': judgeForm, 'path': 'list'})
        return ctx
