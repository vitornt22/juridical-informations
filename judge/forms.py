# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from ijp import settings

from .models import Judge


class JudgeForm(forms.ModelForm):

    class Meta:
        model = Judge
        fields = '__all__'

        labels = {
            'name': 'Nome Completo',
            'cnj': 'CNJ',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': ' Nome Completo',  'class': 'form-control'}),  # noqa
            'cnj': forms.NumberInput(attrs={'placeholder': ' CPF',  'class': 'form-control',  'maxlength': "14"}),  # noqa
        }
