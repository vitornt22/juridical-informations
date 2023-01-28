
from django import forms

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
            'name': forms.TextInput(attrs={'placeholder': ' Nome Completo',
                                           'class': 'form-control'}),
            'cnj': forms.TextInput(
                attrs={'placeholder': ' CNJ',  'class': 'form-control',
                       'data-mask': 'AAAAAAA-AA.AAAA.A.AA.9999',
                       'maxlength': "25"}
            ),
        }
