
from datetime import datetime

from bs4 import BeautifulSoup

from judge.models import Judge
from movement.models import Movement
from parts.models import Part
from process.models import Process


def register_judge(name):
    judge = Judge(name=name)
    judge.save()
    return judge


def register_part(tags, process):
    tags = tags.find_all('li')
    for i in tags:
        name = i.span.text.split('\n')[1].strip()
        category = ''
        aux = i.find_all('span', {'class': 'badge'})
        for j in aux:
            category += j.string.strip()+' '

        part = Part(name=name, category=category)
        part.save()
        process.parts.add(part)


def register_movement(tags, process):
    # select just tr tags  that are movement
    tags = tags.tbody.find_all('tr')[0:-2]

    for i in tags:
        aux = i.find_all('td')
        if len(aux) == 3:
            d = aux[0].string
            date = datetime.strptime(str(d), '%d/%m/%Y').date()
            description = aux[2].string.replace('  ', '')
            movement = Movement(
                date=date,  description=description, process=process)
            movement.save()


def set_tags(tags):
    # save number and status of process
    number_process = tags[0].h4.text.replace('\n', ' ').strip()
    status = None

    # getting the status of process
    try:
        status = 'Ativo' in tags[0].h4.span.string
    except:  # noqa
        status = False

    # separating and  saving a most of the attrs to add into Process Model
    part1 = tags[1:3]

    # part1 HTML= 'classe', 'orgao', 'assunto', 'foro', 'vara', 'comarca'
    # part2  HTML= 'juiz','distribuição', 'controle', 'area', 'valor'

    # getting attrs of html
    list1 = ['' if i.string ==
             '---' else i.string for i in part1[0].find_all(['span'])]
    list2 = []

    for i in part1[1].find_all('div', {'class': 'col-2'}):
        try:
            a = i.span.string
        except:  # noqa
            a = i.div.string
        list2.append('' if '---' in a else a)

    # removing spaces in the string and convert str to float
    list2[-1] = float((list2[-1].replace('R$', '').strip()
                       ).replace('.', '').replace(',', '.'))

    # create Model judeg to assign in model process
    judge = register_judge(list2[0])
    distribution = datetime.strptime(str(list2[1]), '%d/%m/%Y').date()
    if Process.objects.filter(number=number_process).exists():
        return False
    else:
        process = Process(
            number=number_process,
            class_process=list1[0],
            organ=list1[1],
            subject=list1[2],
            forum=list1[3],
            court=list1[4],
            county=list1[5],
            judge=judge,
            distribution=distribution,
            controll=list2[2],
            area=list2[3],
            value=list2[4],
            status=status
        )

        process.save()

        register_part(tags[3], process)
        register_movement(tags[4], process)

        process.save()
        return True


def register_process(file):
    obj = BeautifulSoup(file.read(), "html.parser")
    split = obj.find_all('div', {"class": "row"})[:5]
    value = set_tags(split)
    return value
