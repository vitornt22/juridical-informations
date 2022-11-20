# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from ijp import settings

from .models import Process


class ProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = '__all__'

        labels = {
            'number': 'Nº do Processo',
            'class_project': 'Classe',
            'court': 'Vara',
            'forum': 'Foro',
            'subject': 'Assunto',
            'county': 'Comarca',
            'judge': 'Juiz',
            'value': 'Valor da Ação',
            'organ': 'Orgão',
            'area': 'Área',
            'controll': 'Controle',
        }

        widgets = {
            'id': forms.HiddenInput(),
            'class_project': forms.TextInput(attrs={'placeholder': ' Classe',  'class': 'form-control', 'class': 'form-control'}),  # noqa
            'number': forms.TextInput(attrs={'placeholder': ' Nº do Processo',  'class': 'form-control'}),  # noqa
            'court': forms.TextInput(attrs={'placeholder': ' Vara',  'class': 'form-control'}),  # noqa
            'forum': forms.TextInput(attrs={'placeholder': ' Foro',  'class': 'form-control'}),  # noqa
            'subject': forms.TextInput(attrs={'placeholder': ' Assunto',  'class': 'form-control'}),  # noqa
            'county': forms.TextInput(attrs={'placeholder': ' Comarca', 'class': 'form-control'}),  # noqa
            'judge': forms.TextInput(attrs={'placeholder': ' Juiz',  'class': 'form-control'}),  # noqa
            'value': forms.NumberInput(attrs={'placeholder': ' Valor',  'class': 'form-control'}),  # noqa
            'organ': forms.TextInput(attrs={'placeholder': ' Orgão',  'class': 'form-control'}),  # noqa
            'area': forms.TextInput(attrs={'placeholder': ' Área',  'class': 'form-control'}),  # noqa
            'controll': forms.TextInput(attrs={'placeholder': ' Controller',  'class': 'form-control'}),  # noqa
        }


'''
    def clean_date(self):
        date = self.cleaned_data.get('date')
        hoje = datetime.date.today()

        if date == None:
            date = hoje

        if date > hoje or date.month != hoje.month:
            raise ValidationError((
                'Data indisponivel'
            ),
                code='invalid'
            )
        return date
'''