# flake8: noqa
from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from judge.forms import JudgeForm
from judge.models import Judge
from movement.forms import MovementForm
from movement.models import Movement
from parts.forms import PartForm
from parts.models import Part
from process.forms import ProcessForm
from process.models import Process


class ProcessDetails(View):

    def addParts(self, process):
        parts = self.request.POST.getlist('parts')
        print("LEN", len(parts))
        judge = self.request.POST.get('judge')
        if len(judge) > 0:
            process.judge = Judge.objects.get(id=judge)
        process.save()
        if parts[0] != '':
            parts = parts[0].split(',')

            print("OPSSSS", parts)

            for i in parts:
                if i != "'":
                    part = Part.objects.filter(id=int(i)).first()
                    print("part "+str(i)+" " + str(part))
                    process.parts.add(part)
        print("mY PARTSSSSSSSSSS", process.parts.all())
        process.save()

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
        return render(
            self.request,
            html, context={
                'form': form, 'parts': parts, 'judges': judges,
                'active': 1, 'tag': 'Projeto', 'back': 'process:list',
                'partForm': partForm, 'id': id, 'judgeForm': judgeForm,
                'path': path, 'judgeSelect': judgeSelect, 'myParts': myParts,
                'movements': movements, 'movementForm': movementForm
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
        process = self.get_process(id)
        form = ProcessForm(instance=process)
        html = 'adm/process/processRegister.html' if id is None else 'adm/process/processDetail.html'
        return self.render_process(form, html, id, process)

    def post(self, request, id=None):
        process = self.get_process(id)
        form = ProcessForm(request.POST or None,
                           instance=process)

        if form.is_valid():
            # now form is valid and i can to save it
            process = form.save(commit=False)
            # now i can make changes in object edited

            self.addParts(process)

            process.save()

            if id is not None:
                messages.success(request, 'Processo Editado  com sucesso!')
                return redirect('process:detail', id)
            else:
                messages.success(
                    request, 'Processo Cadastrado com sucesso!')
                return redirect('process:register')
        else:
            print('no')

        html = 'adm/process/processRegister.html' if id is None else 'adm/process/processDetail.html'

        return self.render_process(form, html, id, process)


# dont forget add login required later
class ProcessDelete(ProcessDetails):

    def get(self, request, id=None):
        process = self.get_process(id)
        process.delete()
        messages.success(self.request, 'Deletado com sucesso')
        return redirect('process:list')


class DeleteProcessPart(ProcessDetails):

    def get(self, request, id=None, idPart=None):
        print("OOAOOOAOAOO")
        process = Process.objects.filter(id=id).first()
        print("parts", process)
        if process != None:
            print("ola")
            part = process.parts.get(id=idPart)
            process.parts.remove(part)
            messages.success(
                self.request, 'Parte desligada com sucesso com sucesso')
        return redirect('process:detail', id)


class ProcessList(ListView):
    model = Process
    context_object_name = 'processes'
    ordering = ['-distribution']
    template_name = 'adm/process/processList.html'

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)
        if search:
            qs = qs.filter(Q(
                Q(number__icontains=search) |
                Q(court__icontains=search) | Q(forum__icontains=search) |
                Q(judge__name__icontains=search) | Q(class_project__icontains=search) |
                Q(subject__icontains=search) | Q(organ__icontains=search) |
                Q(area__icontains=search) | Q(county__icontains=search)

            ))

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 1, 'tag': 'Processo', })
        return ctx
