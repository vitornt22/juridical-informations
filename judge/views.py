# Create your views here.
# flake8: noqa
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from .forms import JudgeForm
from .models import Judge


class JudgeDetails(View):

    def render_judge(self, form, html, id):
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
        print("MYY PARTTTTTT")
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
                    request, 'Judgee  Editada  com sucesso!')
            else:
                messages.success(
                    request, 'Judgee Cadastrada com sucesso!')
        else:
            print('no')

        if id is not None:
            html = 'adm/judge/judgeDetail.html'
        else:
            return redirect('process:register')

        return self.render_judge(form, html, id)


# dont forget add login required later
class JudgeDelete(JudgeDetails):

    def get(self, request, id=None):
        print("JUDGDGSGG")
        judge = self.get_judge(id)
        name = judge.category+': ' + judge.name
        judge.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect('judge:list')


class JudgeList(ListView):
    model = Judge
    context_object_name = 'judges'
    ordering = ['-id']
    template_name = 'adm/judge/judgesList.html'

    def get_queryset(self, *args, **kwargs):
        # search= self.request.query_param.get
        qs = super().get_queryset(*args, **kwargs)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 3, 'tag': 'Juiz'})
        return ctx
