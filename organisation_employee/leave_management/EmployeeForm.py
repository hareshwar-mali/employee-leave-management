from django import forms
from .models import EmployeeProfile

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["first_name", "last_name", "phone_number", "password", "status", "total_cs_leaves", "total_e_leaves"]
