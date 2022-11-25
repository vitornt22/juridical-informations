# flake8: noqa
from random import randint

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from judge.forms import JudgeForm
from judge.models import Judge
from movement.forms import MovementForm
from movement.models import Movement
from parts.forms import PartForm
from parts.models import Part
from process.forms import ProcessForm
from process.models import Process
from utils.process_create_functions import addParts, generate_number_process


class ProcessUpdateView(UpdateView):
    model = Process
    form_class = ProcessForm
    template_name = 'adm/process/processDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = context['process']

        print('CONTEXT JEYS', context.keys())
        context['movements'] = Movement.objects.filter(process=process)
        context['movementForm'] = MovementForm()
        context['partForm'] = PartForm()
        context['number'] = None if process is None else process.number
        context['judgeForm'] = JudgeForm()
        context['judgeSelect'] = process.judge
        context['judges'] = Judge.objects.all()
        p = Part.objects.all()
        myParts = None if process is None else process.parts.all()
        context['parts'] = p if myParts is None else p.difference(myParts)
        return context


class ProcessCreateView(CreateView):
    model = Process
    form_class = ProcessForm
    context_object_name = 'form'
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:list'

    def form_valid(self, form):
        process = form.save(commit=False)
        addParts(self, process)
        process.number = generate_number_process(self)
        messages.success(self.request, 'Processo registrado com sucesso!')
        process.save()
        return redirect('process:register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parts'] = Part.objects.all()
        context['partForm'] = PartForm()
        context['judgeForm'] = JudgeForm()
        context['judges'] = Judge.objects.all()
        return context


class ProcessDetailView(DetailView):
    model = Process
