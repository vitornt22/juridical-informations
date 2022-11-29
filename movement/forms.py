# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from juridical_processes_manager import settings

from .models import Movement


class MovementForm(forms.ModelForm):

    date = forms.DateField(label="Data", required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=forms.DateInput(format="%d/%m/%Y", attrs={'readOnly': False, 'class': 'form-control', 'id': 'startLocationID', 'data-mask': '99/99/9999'}))

    class Meta:
        model = Movement
        exclude = ['process']

        labels = {
            'description': 'Descrição',

        }

        widgets = {
            'description': forms.Textarea(attrs={'placeholder': ' Descrição',  'class': 'form-control',  'maxlength': "500"}),  # noqa
        }
