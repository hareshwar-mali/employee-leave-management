from django.contrib import admin
from .models import EmployeeProfile, EmployeeLeave


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'first_name', 'last_name', 'phone_number', 'password', 'status', 'total_cs_leaves',
        'total_e_leaves')
    search_fields = ('first_name', 'last_name', 'phone_number', 'user__username')
    list_filter = ('status',)


@admin.register(EmployeeLeave)
class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('leave_type', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__phone_number')
