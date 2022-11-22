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

    # this method define route redirect accordingly with request
    def calculate_redirect_route(self, path):
        # if post is to create
        if id is None:
            # if the request was made on the process register screen
            # redirect to this screen
            if path == 'processo':
                return redirect('process:register')
            # if the request was made on the process detail
            # redirect to this same screen
            elif 'editar' in path:
                idProcess = int(path.replace('editar', ''))
                print('myInt', idProcess)
                return redirect('process:detail', idProcess)
            # if the conditions above don work, its cause the request was made
            # part list screen, and this method redirect to this same screen
            else:
                return redirect('part:list')

    # GET  request method
    def get(self, request, id=None):
        print("diiiiidiidi", id)
        html = 'adm/process/processRegister.html' if id is None else 'adm/judge/judgeDetail.html'
        judge = self.get_judge(id)

        form = JudgeForm(instance=judge or None)
        return self.render_judge(form, html, id)

    # POST request method
    def post(self, request, id=None, path=None):
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

        # define a possible redirect route
        self.calculate_redirect_route()

        # if method above don't work, to go  to render template
        html = 'adm/judge/judgeDetail.html'

        return self.render_judge(form, html, id)


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
