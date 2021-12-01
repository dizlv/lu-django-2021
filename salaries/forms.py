from django import forms

from salaries import models


class SalaryEntryForm(forms.ModelForm):
    class Meta:
        model = models.SalaryEntry

        fields = (
            'first_name',
            'second_name',
            'birth_day',
            'amount',
        )


class FileUploadForm(forms.Form):
    file = forms.FileField()
