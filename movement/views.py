# Create your views here.
# flake8: noqa
from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from .forms import MovementForm
from .models import Movement


class MovementDetails(View):

    def render_movement(self, form, html, id, idP):
        print('entra aqui')
        return render(self.request, html, context={'form': form,
                                                   'active': 3, 'tag': 'Projeto',
                                                   'back': 'movement:list',
                                                   'id': id})

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
        print("diiiiidiidi", id)
        html = 'adm/process/processRegister.html' if id is None else 'adm/movement/processDetail.html'
        movement = Movement.objects.filter(id=id).first()

        form = MovementForm(instance=movement or None)
        return self.render_movement(form, html, id)

    def post(self, request, id=None, idProcess=None):
        movement = self.get_movement(id)
        print('entrando POST')
        form = MovementForm(request.POST, request.FILES, instance=movement)

        if form.is_valid():
            # now form is valid and i can to save it
            p = form.save(commit=False)
            p.process = id
            # now i can make changes in object edited
            p.save()
            if id is not None:
                messages.success(
                    request, 'Juiz  Editado  com sucesso!')
            else:
                messages.success(
                    request, 'Juiz Cadastrado com sucesso!')

        return redirect('process:detail', id)


# dont forget add login required later
class MovementDelete(MovementDetails):
    def get(self, request, id=None):
        print("DELETEEE")
        movement = self.get_movement(id)
        name = movement.name
        movement.delete()
        messages.success(self.request, name+'(a) Deletado com sucesso')
        return redirect('movement:list')
