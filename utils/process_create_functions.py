
from django.db.models import Q
from django.shortcuts import redirect

from judge.models import Judge
from parts.models import Part


def redirect_part_register(self):
    if self.request.path == '/process/partes/registrar/':
        return redirect('process:register')


def consult_registered_data(request):
    # struct to dont load all objects Judges and Parts
    if request.is_ajax():
        term = request.GET.get('term')
        term_parts = request.GET.get('search')

        if term:
            judges = Judge.objects.all().filter(name__icontains=term)
            response_content = list(judges.values())

        elif term_parts:
            parts = Part.objects.all().filter(
                Q(Q(name__icontains=term_parts) |
                  Q(category__icontains=term_parts)
                  )
            )
            response_content = list(parts.values())
        return response_content
