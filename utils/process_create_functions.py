from random import randint

from django.shortcuts import redirect

from judge.models import Judge
from parts.models import Part
from process.models import Process


def redirect_part_register(self):
    if self.request.path == '/process/partes/registrar/':
        print('ola')
        return redirect('process:register')


def generate_number_process(self):
    verify = True
    number = 0
    while (verify):
        number = randint(100000, 999999)
        if Process.objects.filter(number=number).exists() is False:
            verify = False
    return number


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
