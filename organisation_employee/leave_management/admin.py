from django.contrib import admin

from .models import EmployeeProfile, EmployeeLeave


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmployeeProfile._meta.fields]


class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmployeeLeave._meta.fields]


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(EmployeeLeave, EmployeeLeaveAdmin)
