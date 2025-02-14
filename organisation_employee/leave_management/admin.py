from django.contrib import admin

from .models import EmployeeProfile, EmployeeLeave

# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(EmployeeLeave)
