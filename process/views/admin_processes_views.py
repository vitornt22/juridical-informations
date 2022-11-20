# flake8: noqa
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from parts.forms import PartForm
from parts.models import Part
from process.forms import ProcessForm
from process.models import Process


class ProcessDetails(View):

    def render_process(self, form, html, id=None):
        partForm = PartForm()
        jugdes = Part.objects.filter(category="Juiz")
        authors = Part.objects.filter(category="Autor")
        defendants = Part.objects.filter(category="Réu")
        print('entra aqui')
        return render(
            self.request,
            html, context={
                'form': form,
                'active': 1, 'tag': 'Projeto', 'back': 'process:list',
                'partForm': partForm, 'judges': jugdes, 'authors': authors,
                'defendants': defendants, 'id': id,
            })

    def get_process(self, id=None):
        process = None
        if id is not None:
            print("NOT NONE")
            process = Process.objects.filter(
                id=id
            ).first()

            if not process:
                print("NENBNSNSBA")
                raise Http404()

        return process

    def get(self, request, id=None):
        print('here')

        process = self.get_process(id)
        print("GET MY PROJECT", process)
        form = ProcessForm(instance=process)
        html = 'adm/processRegister.html' if id is None else 'adm/processDetail.html'
        print(html)
        return self.render_process(form, html, id)

    def post(self, request, id=None):
        process = self.get_process(id)
        print('entrando POST')
        print("my request", request.POST.get(
            'register'))
        form = ProcessForm(request.POST or None,
                           instance=process)
        judge = request.POST.get('judge')
        print("MY JUIZ", judge)

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            # now i can make changes in object edited
            p.save()

            if id is not None:
                messages.success(request, 'Processo Editado  com sucesso!')
                return redirect(reverse('process:detail', id))
            else:
                messages.success(request, 'Processo Cadastrado com sucesso!')
                return redirect(reverse('process:register'))
        else:
            print('no')

        html = 'adm/processRegister.html' if id is None else 'adm/processDetail.html'

        return self.render_process(form, html, id)


# dont forget add login required later
class ProcessDelete(ProcessDetails):
    def post(self, request, id=None):
        process = self.get_process(self.request.POST.ger('id'))
        process.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect()


class ProcessList(ListView):
    model = Process
    context_object_name = 'processes'
    ordering = ['-distribution']
    template_name = 'adm/processList.html'

    def get_queryset(self, *args, **kwargs):
        # search= self.request.query_param.get
        qs = super().get_queryset(*args, **kwargs)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 1, 'tag': 'Processo'})
        return ctx
