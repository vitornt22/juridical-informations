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

from .forms import PartForm
from .models import Part


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class PartDetails(View):

    # render request template
    def render_part(self, form, html, id, idP):
        active = 2
        path = 'part:list'
        # if id process is not None, set path with value to redirect
        # to process detail  page, when click back button on html template
        if idP is not None:
            path = 'process:detail'
            active = 1
        context = {'form': form,
                   'active': active, 'tag': 'Projeto',
                   'back': 'part:list',
                   'id': id, 'idP': idP, 'path': path}
        return render(self.request, html, context)

    # get  instance of part if it exists
    def get_part(self, id=None):
        part = None
        if id is not None:
            part = Part.objects.filter(
                pk=id
            ).first()

            if not part:
                raise Http404()
        print("MYY PARTTTTTT")
        return part

    # GET method
    def get(self, request, id=None, editId=None, idP=None):
        html = 'adm/parts/processRegister.html' if id is None else 'adm/parts/partDetail.html'
        part = self.get_part(id)
        form = PartForm(instance=part or None)
        return self.render_part(form, html, id, idP)

    # POST method
    def post(self, request, id=None, path=None,  idP=None):
        part = self.get_part(id)
        form = PartForm(request.POST, request.FILES, instance=part)

        cpf = form.data['cpf']
        if Part.objects.filter(cpf=cpf).exists:
            messages.error(request, 'CPF existente, tente novamente')

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            # now i can make changes in object edited
            p.save()

            # check is post is to creat or edit part, and send message to  request template
            if id is not None:
                messages.success(
                    request, 'Parte  Editada  com sucesso!')
            else:
                messages.success(
                    request, 'Parte Cadastrada com sucesso!')

        # check if post is to create or edit
        if id is None:
            # if request was been made in process page, redirect to this same page
            # else, redirect to list parts page
            if path == 'processo':
                print('MY PATH', request.path)
                return redirect('process:register')
            elif 'edit' in path:
                idProcess = int(path.replace('editar', ''))
                print("ID PROCESS", idProcess)
                return redirect('process:detail', idProcess)
            else:
                return redirect('part:list')

        print('chegando ate aqui')
        html = 'adm/parts/partDetail.html'
        return self.render_part(form, html, id, idP)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class PartDelete(PartDetails):
    # method to delete part instance
    def get(self, request, id=None):
        part = self.get_part(id)
        name = part.category+': ' + part.name
        part.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect('part:list')


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class PartList(ListView):
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
        ctx.update({"active": 2, 'tag': 'Parto',
                   'path': 'list', 'partForm': partForm})
        return ctx
