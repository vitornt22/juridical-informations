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
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from process.forms import ProcessForm

from .forms import JudgeForm
from .models import Judge


class JudgeCreateView(CreateView):
    model = Judge
    form_class = JudgeForm
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:list'

    def form_valid(self, form):
        judge = form.save(commit=False)
        if Judge.objects.filter(cnj=judge.cnj):
            messages.error(self.request, 'CNJ existente, tente novamente')
        judge.save()
        messages.success(self.request, 'Juiz registrada com sucess')
        if self.request.path == '/process/partes/registrar/':
            print('ola')
            return redirect('process:register')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProcessForm()
        context['partForm'] = JudgeForm()
        context['judgeForm'] = JudgeForm()
        return context

    def post(self, request, *args, **kwargs):
        post = super().post(request, *args, **kwargs)
        return post


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeDetails(View):

    # function to render html template of request
    def render_judge(self, form, html, id, idP):
        context = {'form': form,
                   'active': 3, 'tag': 'Projeto',
                   'back': 'judge:list',
                   'id': id}
        return render(self.request, html, context)

    # get instance of object if it exists
    def get_judge(self, id=None):
        judge = None
        if id is not None:
            judge = Judge.objects.filter(
                pk=id
            ).first()

            if not judge:
                raise Http404()
        return judge

    # GET  request method
    def get(self, request, id=None, idP=None):
        html = 'adm/process/processRegister.html' if id is None else 'adm/judge/judgeDetail.html'
        judge = self.get_judge(id)

        form = JudgeForm(instance=judge or None)
        return self.render_judge(form, html, id, idP)

    # POST request method
    def post(self, request, id=None, path=None, idP=None):
        judge = self.get_judge(id)
        form = JudgeForm(request.POST, request.FILES, instance=judge)

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            # now i can make changes in object edited
            p.save()
            # check if post is create or editid and send message to template
            if id is not None:
                messages.success(
                    request, 'Juiz  Editado  com sucesso!')
            else:
                messages.success(
                    request, 'Juiz Cadastrado com sucesso!')

        if id is None:
            # if request was been made in process page, redirect to this same page
            # else, redirect to list parts page
            if path == 'processo':
                return redirect('process:register')
            elif 'edit' in path:
                idProcess = int(path.replace('editar', ''))
                return redirect('process:detail', idProcess)
            else:
                return redirect('judge:list')

        # if method above don't work, to go  to render template
        html = 'adm/judge/judgeDetail.html'

        return self.render_judge(form, html, id, idP)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class JudgeDelete(JudgeDetails):
    # methodo GET to delete any judge instance passed by request
    def get(self, request, id=None):
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
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)
        if search is not None:
            qs = qs.filter(Q(Q(name__icontains=search)
                           | Q(cnj__icontains=search)))
        return qs

    def get_context_data(self, *args, **kwargs):
        judgeForm = JudgeForm()
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 3, 'tag': 'Juiz',
                   'judgeForm': judgeForm, 'path': 'list'})
        return ctx
