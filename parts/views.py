# flake8: noqa
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from .forms import PartForm
from .models import Part


class PartDetails(View):

    def render_part(self, form, html, id, idP):
        print('entra aqui')
        active = 2
        path = 'part:list'
        if 'editarParte/process' in self.request.path:
            path = 'process:detail'
            active = 1
        return render(self.request, html, context={'form': form,
                                                   'active': active, 'tag': 'Projeto',
                                                   'back': 'part:list',
                                                   'id': id, 'idP': idP, 'path': path})

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

    def get(self, request, id=None, editId=None, idP=None):
        print("diiiiidiidi", id)
        html = 'adm/parts/processRegister.html' if id is None else 'adm/parts/partDetail.html'
        part = self.get_part(id)

        form = PartForm(instance=part or None)
        return self.render_part(form, html, id, idP)

    def post(self, request, id=None, path=None, editId=None, idP=None):
        part = self.get_part(id)
        print('entrando POST')
        form = PartForm(request.POST, request.FILES, instance=part)
        print("pathh", path)

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            # now i can make changes in object edited
            p.save()
            if id is not None:
                messages.success(
                    request, 'Parte  Editada  com sucesso!')
            else:
                messages.success(
                    request, 'Parte Cadastrada com sucesso!')

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
        html = 'adm/parts/partDetail.html'
        return self.render_part(form, html, id, idP)


# dont forget add login required later
class PartDelete(PartDetails):

    def get(self, request, id=None):
        part = self.get_part(id)
        name = part.category+': ' + part.name
        part.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect('part:list')


class PartList(ListView):
    model = Part
    context_object_name = 'parts'
    ordering = ['-id']
    template_name = 'adm/parts/partsList.html'

    def get_queryset(self, *args, **kwargs):
        # search= self.request.query_param.get
        qs = super().get_queryset(*args, **kwargs)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 2, 'tag': 'Parto'})
        return ctx
