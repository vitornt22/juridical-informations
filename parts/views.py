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

    def render_part(self, form, html):
        print('entra aqui')
        return render(self.request, html, context={'form': form,
                                                   'active': 2, 'tag': 'Projeto',
                                                   'back': 'part:list'})

    def get_part(self, id=None):
        part = None
        if id is not None:
            part = Part.objects.filter(
                pk=id
            ).first

            if not part:
                raise Http404()
        return part

    def get(self, request, id=None):
        html = 'adm/processRegister.html' if id is None else 'adm/processDetail.html'
        part = self.get_part(id)

        form = PartForm(instance=part or None)
        return self.render_part(form, html)

    def post(self, request, id=None, path=None):
        part = self.get_part(id)
        print('entrando POST')
        form = PartForm(request.POST or None, instance=part)
        print("PATH", path)

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            # now i can make changes in object edited
            p.save()

            messages.success(request, 'Parto salvo com sucesso!')
            route = 'parte:register' if path == 'parte' else 'process:register'
            return redirect(reverse(route, args=(id)))
        else:
            print('no')

        html = 'adm/partRegister.html' if id is None else 'adm/partDetail.html'

        return self.render_part(form, html)


# dont forget add login required later
class PartDelete(PartDetails):
    def post(self, request, id=None):
        part = self.get_part(self.request.POST.ger('id'))
        part.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect()


class PartList(ListView):
    model = Part
    context_object_name = 'parts'
    ordering = ['-id']
    template_name = 'adm/partsList.html'

    def get_queryset(self, *args, **kwargs):
        # search= self.request.query_param.get
        qs = super().get_queryset(*args, **kwargs)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 1, 'tag': 'Parto'})
        return ctx
