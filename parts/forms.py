
from django import forms

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
            'name': forms.TextInput(attrs={
                'placeholder': ' Nome Completo',
                'class': 'form-control'}
            ),
            'category': forms.TextInput(attrs={
                'placeholder': ' Categoria ',
                'class': 'form-control'}
            ),
        }
