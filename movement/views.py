# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, UpdateView

from process.models import Process

from .forms import MovementForm
from .models import Movement


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class MovementCreateView(CreateView):
    model = Movement
    form_class = MovementForm
    template_name = 'adm/process/processRegister.html'
    success_url = 'process:detail'

    def form_invalid(self, form):
        try:
            messages.error(self.request, 'Erro ao registrar, tente novamente')
            return super().form_valid(form)
        except:
            messages.error(self.request, 'Erro: Data pode ser inválida')
            idProcess = self.kwargs.get('idProcess')
            return redirect('process:detail', idProcess)

    def form_valid(self, form):
        movement = form.save(commit=False)
        movement.save()
        idProcess = self.kwargs.get('idProcess')
        if idProcess is not None:
            movement.process = Process.objects.filter(id=idProcess).first()
            movement.save()
        messages.success(self.request, 'Movimentação registrada com sucesso')

    def post(self, request, idProcess=None, *args, **kwargs):
        super().post(request, idProcess, *args, **kwargs)
        return redirect('process:detail', idProcess)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class MovementUpdateView(UpdateView):
    model = Movement
    form_class = MovementForm
    template_name = 'adm/movement/movementDetail.html'
    success_url = 'movement:detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['idProcess'] = self.kwargs.get('idProcess')
        return context

    def form_valid(self, form):
        movement = form.save(commit=False)
        movement.save()
        messages.success(self.request, 'Dados Editados')
        return redirect('process:detail', movement.process.id)


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class MovementDeleteView(View):
    # specify the model you want to use
    def get(self, request, *args, **kwargs):
        movement = Movement.objects.filter(id=kwargs.get('pk')).first()
        id = movement.process.id
        if movement:
            messages.success(request, 'Movimentação deletada com sucesso')
            movement.delete()
        else:
            messages.error(request, 'Erro ao tentar deletar')
            raise Http404()
        return redirect('process:detail', id)
