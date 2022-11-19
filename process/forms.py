# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from ijp import settings

from .models import Process


class ProcessForm(forms.ModelForm):
    distribution = forms.DateField(label="Data", required=False, input_formats=settings.DATE_INPUT_FORMATS,
                                   widget=forms.DateInput(format="%d/%m/%Y", attrs={'readOnly': False, 'id': 'Distribuição', 'data-mask': '99/99/9999'}))

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

        }

        widgets = {
            'id': forms.HiddenInput(),
            'class_project': forms.TextInput(attrs={'placeholder': ' Classe', 'required': 'True'}),  # noqa
            'number': forms.TextInput(attrs={'placeholder': ' Nº do Processo', 'required': 'True'}),  # noqa
            'court': forms.TextInput(attrs={'placeholder': ' Vara', 'required': 'True'}),  # noqa
            'forum': forms.TextInput(attrs={'placeholder': ' Foro', 'required': 'True'}),  # noqa
            'subject': forms.TextInput(attrs={'placeholder': ' Assunto', 'required': 'True'}),  # noqa
            'county': forms.TextInput(attrs={'placeholder': ' Comarca', 'required': 'True'}),  # noqa
            'judge': forms.TextInput(attrs={'placeholder': ' Juiz', 'required': 'True'}),  # noqa
            'value': forms.NumberInput(attrs={'placeholder': ' Valor', 'required': 'True'}),  # noqa

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
