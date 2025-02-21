from django import forms
from .models import EmployeeProfile
from django.core.exceptions import ValidationError
import re


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["first_name", "last_name", "phone_number", "password", "status", "total_cs_leaves", "total_e_leaves"]

    # validate phone number
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        pattern = r"^[7-9]\d{9}$"
        if not re.match(pattern, phone_number):
            raise ValidationError("Phone number must be exactly 10 digits and start with 7, 8, or 9.")

        # Check if the phone number already exists in the database
        if EmployeeProfile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("An employee with this phone number already exists.")

        return phone_number
