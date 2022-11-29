import datetime

from django.http import HttpResponse
from xlwt import Workbook


def export_csv(qs):
    list_qs = qs.values_list()
    date = str(datetime.date.today())
    filename = 'processos-'+date+'.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    fields = ['id', 'Nº', 'Classe', 'Vara', 'Foro', 'Assunto', 'Orgão', 'Area',
              'COMARCA', 'Controle', 'Distribuição', 'Juiz', 'Valor', 'Status']

    wb = Workbook(encoding='utf-8')
    processes = wb.add_sheet('Processos')

    # add columns of processs
    for i in range(len(fields)):
        processes.write(0, i, str(fields[i]))
    # add column values to exportt
    row = 1
    for i in list_qs:
        column = 0
        for j in i:
            if (str(i[column]) != 'None'):
                processes.write(row, column, str(i[column]))
            column += 1
        row += 1
    wb.save(response)

    return response
