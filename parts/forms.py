# flake8: noqa: E501
import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Part


class PartForm(forms.ModelForm):

    class Meta:
        model = Part
        exclude = ['process']

        labels = {
            'name': 'Nome Completo',
            'category': 'Categoria da parte',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': ' Nome Completo',  'class': 'form-control'}),  # noqa
            'category': forms.TextInput(attrs={'placeholder': ' Categoria ',  'class': 'form-control'}),  # noqa
        }
