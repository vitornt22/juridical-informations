# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from juridical_processes_manager import settings

from .models import Process


class ProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        exclude = ['number']

        labels = {
            'class_process': 'Classe',
            'court': 'Vara',
            'forum': 'Foro',
            'subject': 'Assunto',
            'county': 'Comarca',
            'value': 'Valor da Ação',
            'organ': 'Orgão',
            'area': 'Área',
            'controll': 'Controle',

        }

        widgets = {
               'id': forms.HiddenInput(),
               'class_process': forms.TextInput(attrs={'placeholder': ' Classe',  'class': 'form-control', 'class': 'form-control'}),  # noqa
               'court': forms.TextInput(attrs={'placeholder': ' Vara',  'class': 'form-control'}),  # noqa
               'forum': forms.TextInput(attrs={'placeholder': ' Foro',  'class': 'form-control'}),  # noqa
               'subject': forms.TextInput(attrs={'placeholder': ' Assunto',  'class': 'form-control'}),  # noqa
               'county': forms.TextInput(attrs={'placeholder': ' Comarca', 'class': 'form-control'}),  # noqa
               'value': forms.NumberInput(attrs={'placeholder': ' Valor',  'class': 'form-control'}),  # noqa
               'organ': forms.TextInput(attrs={'placeholder': ' Orgão',  'class': 'form-control'}),  # noqa
               'area': forms.TextInput(attrs={'placeholder': ' Área',  'class': 'form-control'}),  # noqa
               'controll': forms.TextInput(attrs={'class': 'form-control'}),  # noqa
                'judge': forms.Select(attrs={'placeholder': ' Juiz',   'id': "multipleSelect", 'name': "judge", 'class': "", 'required': 'true',  'multiple': 'false', 'name': "native-select",
                'placeholder': "Selecionar Partes", 'data-search': "true",  "data-silent-initial-value-set": "true"}),  # noqa

           }
