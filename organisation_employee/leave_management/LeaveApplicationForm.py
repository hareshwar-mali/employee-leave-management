from django import forms
from .models import EmployeeLeave


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeave
        fields = ['leave_type', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date.")
        return cleaned_data
