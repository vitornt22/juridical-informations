# Create your views here.
# flake8: noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.list import ListView

from process.models import Process

from .forms import MovementForm
from .models import Movement


@ method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class MovementDetails(View):

    # method to render template of process movement
    def render_movement(self, form, html, id, idP):
        context = {'form': form,
                   'active': 3, 'tag': 'Projeto',
                   'idProcess': idP,
                   'back': 'movement:list',
                   'id': id}
        return render(self.request, html, context)

    # GET instance of movement if exists
    def get_movement(self, id=None):
        movement = None
        if id is not None:
            movement = Movement.objects.filter(
                pk=id
            ).first()

            if not movement:
                raise Http404()
        return movement

    def get(self, request, id=None, idProcess=None):
        html = 'adm/process/processRegister.html' if id is None else 'adm/movement/movementDetail.html'
        movement = Movement.objects.filter(id=id).first()

        form = MovementForm(instance=movement or None)
        return self.render_movement(form, html, id, idProcess)

    def post(self, request, id=None, idProcess=None):

        movement = self.get_movement(id)
        form = MovementForm(request.POST, request.FILES, instance=movement)

        if form.is_valid():
            # now form is valid and i can to s
            p = form.save(commit=False)

            if idProcess is not None:
                p.process = Process.objects.filter(id=idProcess).first()
            p.save()

            # check if request POST is to create or edit and send message to the
            # respective request template
            if id is not None:
                messages.success(
                    request, 'Juiz  Editado  com sucesso!')
            else:
                messages.success(
                    request, 'Juiz Cadastrado com sucesso!')
        else:
            # if the form is invalid redirect to process detail page
            # where i can work in CRUD of movement
            if id is not None:
                return redirect('movement:detail', idProcess, id)

        return redirect('process:detail', idProcess)


@method_decorator(
    login_required(login_url='process:loginPage', redirect_field_name='next'),
    name='dispatch'
)
class MovementDelete(MovementDetails):
    def get(self, request, id=None):
        movement = self.get_movement(id)
        id = movement.process.id
        movement.delete()
        messages.success(self.request, 'Movimentação Deletada com sucesso')
        return redirect('process:detail', id)
