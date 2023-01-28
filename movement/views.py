# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
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
            redirect_function = super().form_valid(form)
            messages.error(self.request, 'Erro ao registrar, tente novamente')
            return redirect_function
        except redirect_function is None:
            messages.error(self.request, 'Erro: Data pode ser inválida')
            id_process = self.kwargs.get('id_process')
            return redirect('process:detail', id_process)

    def form_valid(self, form):
        movement = form.save(commit=False)
        movement.save()
        id_process = self.kwargs.get('id_process')
        if id_process is not None:
            movement.process = Process.objects.filter(id=id_process).first()
            movement.save()
        messages.success(self.request, 'Movimentação registrada com sucesso')

    def post(self, request, id_process=None, *args, **kwargs):
        super().post(request, id_process, *args, **kwargs)
        return redirect('process:detail', id_process)


@ method_decorator(
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
        context['id_process'] = self.kwargs.get('id_process')
        return context

    def form_valid(self, form):
        movement = form.save(commit=False)
        movement.save()
        messages.success(self.request, 'Dados Editados')
        return redirect('process:detail', movement.process.id)

    def post(self, request, id_process=None, *args, **kwargs):
        super().post(request, id_process, *args, **kwargs)
        return redirect('process:detail', id_process)


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
