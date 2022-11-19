# flake8: noqa
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from process.forms import ProcessForm
from process.models import Process


class ProcessDetails(View):

    def render_process(self, form):
        return render(self.request, 'admin/processDetail.html', context={'form': form, 'active': 1})

    def get_process(self, id=None):
        process = None
        if id is not None:
            process = Process.objects.filter(
                pk=id
            ).first

        if not process:
            raise Http404()

        return process

    def get(self, request, id=None):
        process = self.get_process(id)
        form = ProcessForm(instance=process)
        return self.render_process(form)

    def post(self, request, id=None):
        process = self.get_process(id)
        form = ProcessDetails(data=request.POST or None, instance=process)

        if form.is_valid():
            # now form is valid and i can to save it
            process = form.save(commit=False)
            # now i can make changes in object edited
            process.save()
            messages.success(request, 'Processo salvo com sucesso!')
            # return redirect here
        return self.render_process(form)


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
        ctx.update({"active": 1})
        return ctx
