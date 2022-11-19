# flake8: noqa
from django.shortcuts import render

from .admin_processes_views import ProcessDelete, ProcessDetails, ProcessList


class ProcessClientDetail(ProcessDetails):
    def render_process(self, form):
        return render(self.request, 'admin/processDetail.html', context={'form': form, 'active': "1"})


class ProcessesClientList(ProcessList):
    template_name = 'clients/processesSearched.html'
