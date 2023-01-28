import re

from django import forms
from django.core.exceptions import ValidationError

from judge.models import Judge
from parts.models import Part

from .models import Process


class ProcessForm(forms.ModelForm):

    parts = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'style': 'width:100%;'}),
        queryset=Part.objects.all()
    )

    class Meta:
        model = Process
        fields = '__all__'

        labels = {
            'parts': 'Partes do Processo',
            'class_process': 'Classe',
            'number': 'Nº do Processo',
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
            'number': forms.TextInput(attrs={
                'placeholder': ' Nº do Processo',  'class': 'form-control',
                'maxlength': "25", 'data-mask': '9999999-99.9999.9.99.9999'}
            ),
            'class_process': forms.TextInput(attrs={
                'placeholder': ' Classe',  'class': 'form-control',
                'class': 'form-control'}
            ),
            'court': forms.TextInput(attrs={
                'placeholder': ' Vara',  'class': 'form-control'}
            ),
            'forum': forms.TextInput(attrs={
                'placeholder': ' Foro',  'class': 'form-control'}
            ),
            'subject': forms.TextInput(attrs={
                'placeholder': ' Assunto',  'class': 'form-control'}
            ),
            'county': forms.TextInput(attrs={
                'placeholder': ' Comarca', 'class': 'form-control'}
            ),
            'value': forms.NumberInput(attrs={
                'placeholder': ' Valor',  'class': 'form-control'}
            ),
            'organ': forms.TextInput(attrs={
                'placeholder': ' Orgão',  'class': 'form-control'}
            ),
            'area': forms.TextInput(attrs={
                'placeholder': ' Área',  'class': 'form-control'}
            ),
            'controll': forms.TextInput(attrs={
                'class': 'form-control'}
            ),
            'judge': forms.Select(attrs={
                'style': 'width:100%;', 'placeholder': 'Juiz', 'class': ''}
            ),
        }

    def clean_number(self):
        number = self.cleaned_data['number']
        regex = re.compile(
            r'^[0-9]{7}[-]?[0-9]{2}[.]?[0-9]{4}[.]?[0-9]{1}[.]?[0-9]{2}[.]?[0-9]{4}$')  # noqa

        if not regex.match(number):
            raise ValidationError('Formato não suportado ')

        return number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['judge'].queryset = Judge.objects.none()
        self.fields['parts'].queryset = Part.objects.all()

        if 'judge' in self.data:
            self.fields['judge'].queryset = Judge.objects.all()
        elif 'parts' in self.data:
            self.fields['parts'].queryset = Part.objects.all()
        elif self.instance.id is not None:
            if self.instance.judge is not None:
                self.fields['judge'].queryset = Judge.objects.all().filter(
                    pk=self.instance.judge.id)
            self.fields['parts'].queryset = self.instance.parts.all()
