
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from judge.forms import JudgeForm
from judge.models import Judge
from movement.forms import MovementForm
from movement.models import Movement
from parts.forms import PartForm
from parts.models import Part
from process.forms import ProcessForm
from process.models import Process
from utils.export_csv import export_csv
from utils.process_create_functions import consult_registered_data
from utils.web_scrapping import register_process


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class ProcessUpdateView(UpdateView):
    model = Process
    form_class = ProcessForm
    template_name = 'adm/process/processDetail.html'
    success_url = 'process:detail'

    def get(self, request, *args: str, **kwargs):
        a = super().get(request, *args, **kwargs)
        # struct to dont load all objects Judges and Parts
        response_content = consult_registered_data(request)
        if response_content:
            return JsonResponse(response_content, safe=False)

        return a

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = context['process']
        context['movements'] = Movement.objects.filter(
            process=process).order_by('-date')
        context['movement_form'] = MovementForm()
        context['part_form'] = PartForm()
        context['active'] = 1
        context['number'] = None if process is None else process.number
        context['judge_form'] = JudgeForm()
        context['judgeSelect'] = process.judge
        context['judges'] = Judge.objects.all()
        context['partPath'] = 'part:processDetailPart'
        context['judgePath'] = 'judge:processDetailJudge'
        p = Part.objects.all()
        my_parts = None if process is None else process.parts.all()
        context['myParts'] = my_parts
        context['parts'] = p if my_parts is None else p.difference(my_parts)
        return context

    def form_valid(self, form):
        process = form.save(commit=False)
        process.save()
        lista = self.request.POST.getlist('parts')
        process.parts.clear()
        process.parts.add(*[int(i)
                          for i in lista])
        messages.success(self.request, 'Processso Alterado com sucesso')
        id = self.kwargs.get('pk')
        return redirect('process:detail', id)


@method_decorator(
    login_required(login_url='process:loginPage',
                   redirect_field_name='next'),
    name='dispatch'
)
class ProcessCreateView(CreateView):
    model = Process
    form_class = ProcessForm
    context_object_name = 'form'
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:list'

    def get(self, request, *args: str, **kwargs):
        a = super().get(request, *args, **kwargs)

        # struct to dont load all objects Judges and Parts
        response_content = consult_registered_data(request)
        if response_content:
            return JsonResponse(response_content, safe=False)

        return a

    def form_valid(self, form):
        process = form.save(commit=False)
        messages.success(self.request, 'Processo registrado com sucesso!')
        process.save()
        process.parts.add(*[int(i)
                          for i in self.request.POST.getlist('parts')])

        return redirect('process:register')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['parts'] = Part.objects.all()
        context['active'] = 1
        context['part_form'] = PartForm()
        context['judge_form'] = JudgeForm()
        context['partPath'] = 'part:processPartRegister'
        context['judgePath'] = 'judge:registerProcessJudge'
        return context


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'


)
class ProcessList(ListView):
    model = Process
    context_object_name = 'processes'
    ordering = ['-distribution']
    template_name = 'adm/process/processList.html'

    # GET method to list processes or export csv file in adm page
    def get(self,  *args, **kwargs):
        list_process = super().get(*args, **kwargs)
        qs = self.get_queryset()
        request_export = self.request.GET.get('export')
        if request_export:
            file = export_csv(qs)
            return file
        return list_process

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        qs = super().get_queryset(*args, **kwargs)
        if search:
            qs = qs.filter(Q(
                Q(number__icontains=search) | Q(court__icontains=search) |
                Q(forum__icontains=search) | Q(judge__name__icontains=search) |
                Q(class_process__icontains=search) |
                Q(subject__icontains=search) | Q(organ__icontains=search) |
                Q(area__icontains=search) | Q(county__icontains=search)

            ))

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"active": 1})
        return ctx


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class ProcessDeleteView(View):

    def get(self, request, *args, **kwargs):
        part = Process.objects.filter(id=kwargs.get('pk')).first()
        if part:
            messages.success(request, 'Processo deletado com sucesso')
            part.delete()
        else:
            messages.error(request, 'Erro ao tentar deletar')
            raise Http404()

        return redirect('process:list')


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class ShutDownPart(View):
    # method to shut down part of its respective process. OBS: this method
    # dont delete part, just remove of many to many relationship
    def get(self, request, id=None, id_part=None):
        # get process
        process = Process.objects.get(id=id)

        # if process not is null, then get part,
        # remove of relationship, and redirect to process detail page
        if process is not None:
            part = process.parts.get(id=id_part)
            process.parts.remove(part)
            messages.success(
                self.request, 'Parte desligada com sucesso com sucesso')
        return redirect('process:detail', id)


@ login_required(login_url='process:loginPage', redirect_field_name='next')
def register_with_file(request):
    file = request.FILES['file']
    value = register_process(file)
    if value is True:
        messages.success(request, 'Processo Cadastrado com Sucesso ! ')
        return redirect('process:list')
    else:
        messages.error(
            request,
            'Erro ao tentar cadastrar.Arquivo inválido ou o Processo' +
            ' já está Cadastrado'
        )
        return redirect('process:register')
