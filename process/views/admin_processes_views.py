# flake8: noqa
import datetime
import io

import xlwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.list import ListView
from xlwt import Workbook

from judge.forms import JudgeForm
from judge.models import Judge
from movement.forms import MovementForm
from movement.models import Movement
from parts.forms import PartForm
from parts.models import Part
from process.forms import ProcessForm
from process.models import Process


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class ProcessDetails(View):

    # this method add all selected parts to  process
    def addParts(self, process):
        parts = self.request.POST.getlist('parts')
        judge = self.request.POST.get('judge')

        # set select judge to process and save it
        if len(judge) > 0:
            process.judge = Judge.objects.get(id=judge)
        process.save()

        # check if list of parts is not None to add in process
        if parts[0] != '':
            parts = parts[0].split(',')

            # go through the entire list of selected parts
            # and add each one to the request process
            for i in parts:
                if i != "'":
                    part = Part.objects.filter(id=int(i)).first()
                    process.parts.add(part)

        process.save()

    # set necessary objects for template and render it
    def render_process(self, form, html, id, process):
        movements = Movement.objects.filter(process=process)
        movementForm = MovementForm()
        partForm = PartForm()
        judgeForm = JudgeForm()
        judgeSelect = Process.objects.filter(id=id).first()
        judges = Judge.objects.all()
        p = Part.objects.all()
        path = 'processo' if id is None else 'editar'+str(id)
        myParts = None if process is None else process.parts.all()
        parts = p if myParts is None else p.difference(myParts)

        context = {
            'form': form, 'parts': parts, 'judges': judges,
            'active': 1, 'tag': 'Projeto', 'back': 'process:list',
            'partForm': partForm, 'id': id, 'judgeForm': judgeForm,
            'path': path, 'judgeSelect': judgeSelect, 'myParts': myParts,
            'movements': movements, 'movementForm': movementForm
        }

        return render(self.request, html, context)

    # get instance of process if exists
    def get_process(self, id=None):
        process = None
        if id is not None:
            process = Process.objects.filter(
                id=id
            ).first()

            if not process:
                raise Http404()

        return process

    # GET method
    def get(self, request, id=None):
        process = self.get_process(id)
        form = ProcessForm(instance=process)
        html = 'adm/process/processRegister.html' if id is None else 'adm/process/processDetail.html'
        return self.render_process(form, html, id, process)

    # POST method
    def post(self, request, id=None):
        process = self.get_process(id)
        form = ProcessForm(request.POST or None,
                           instance=process)

        if form.is_valid():
            # now form is valid and i can to save it
            process = form.save(commit=False)
            # now i can make changes in object edited
            # calls method to add select objects into processo
            self.addParts(process)

            process.save()

            # check if request post is to create or edit process,
            # and redirect to respective page
            if id is not None:
                messages.success(request, 'Processo Editado  com sucesso!')
                return redirect('process:detail', id)
            else:
                messages.success(
                    request, 'Processo Cadastrado com sucesso!')
                return redirect('process:register')

        html = 'adm/process/processRegister.html' if id is None else 'adm/process/processDetail.html'
        return self.render_process(form, html, id, process)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class ProcessDelete(ProcessDetails):
    # method to delete instance of process model
    def get(self, request, id=None):
        process = self.get_process(id)
        process.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect('process:list')


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class DeleteProcessPart(ProcessDetails):

    # method to shut down part of its respective process. OBS: this method
    # dont delete part, just remove of many to many relationship
    def get(self, request, id=None, idPart=None):
        # get process
        process = Process.objects.filter(id=id).first()

        # if process not is null, then get part,
        # remove of realitionship, and redirect to process detail page
        if process != None:
            part = process.parts.get(id=idPart)
            process.parts.remove(part)
            messages.success(
                self.request, 'Parte desligada com sucesso com sucesso')
        return redirect('process:detail', id)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class ProcessList(ListView):
    model = Process
    context_object_name = 'processes'
    ordering = ['-distribution']
    template_name = 'adm/process/processList.html'

    # method to export processes sheet

    def export(self, qs):
        list_qs = qs.values_list()
        date = str(datetime.date.today())
        filename = 'processos-'+date+'.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        fields = ['id', 'Nº', 'Classe', 'Vara', 'Foro', 'Assunto', 'Orgão', 'Area',
                  'COMARCA', 'Controle', 'Distribuição', 'Juiz', 'Valor', 'Status']

        wb = Workbook(encoding='utf-8')
        processes = wb.add_sheet('Processos')

        # add columns of processs
        for i in range(len(fields)):
            processes.write(0, i, str(fields[i]))
        # add column values to exportt
        row = 1
        for i in list_qs:
            column = 0
            for j in i:
                if (str(i[column]) != 'None'):
                    processes.write(row, column, str(i[column]))
                column += 1
            row += 1
        wb.save(response)

        return response

    # GET method to list processes in adm page
    def get(self,  *args, **kwargs):
        list_process = super().get(*args, **kwargs)
        qs = self.get_queryset()
        file = self.export(qs)
        if self.request.GET.get('export'):
            return file
        return list_process

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)
        if search:
            qs = qs.filter(Q(
                Q(number__icontains=search) |
                Q(court__icontains=search) | Q(forum__icontains=search) |
                Q(judge__name__icontains=search) | Q(class_process__icontains=search) |
                Q(subject__icontains=search) | Q(organ__icontains=search) |
                Q(area__icontains=search) | Q(county__icontains=search)

            ))

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 1, 'tag': 'Processo', })
        return ctx
