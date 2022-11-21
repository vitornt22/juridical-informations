# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from ijp import settings

from .models import Movement


class MovementForm(forms.ModelForm):

    class Meta:
        model = Movement
        exclude = ['process']

        labels = {
            'date': 'Data',
            'description': 'Descrição',

        }

        widgets = {
            'date': forms.DateInput(attrs={'placeholder': ' Data',  'class': 'form-control'}),  # noqa
            'description': forms.Textarea(attrs={'placeholder': ' CPF',  'class': 'form-control',  'maxlength': "500"}),  # noqa
        }
