from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from .EmployeeForm import EmployeeForm
from .LeaveApplicationForm import LeaveApplicationForm
from .models import EmployeeProfile, EmployeeLeave
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils.timezone import now


@login_required
def admin_dashboard(request):
    today = now().date()
    first_day_of_month = today.replace(day=1)
    current_quarter = (today.month - 1) // 3 + 1
    first_day_of_quarter = datetime(today.year, 3 * current_quarter - 2, 1).date()
    financial_year_start = datetime(today.year if today.month >= 4 else today.year - 1, 4, 1).date()

    employees = EmployeeProfile.objects.all().annotate(
        total_sick=Count('employeeleave', filter=Q(employeeleave__leave_type='CS')),
        total_earned=Count('employeeleave', filter=Q(employeeleave__leave_type='E'))
    )

    leave_report = []
    for employee in employees:
        leaves_this_month = EmployeeLeave.objects.filter(
            employee=employee, start_date__range=(first_day_of_month, today)
        ).count()

        leaves_this_quarter = EmployeeLeave.objects.filter(
            employee=employee, start_date__range=(first_day_of_quarter, today)
        ).count()

        leaves_this_year = EmployeeLeave.objects.filter(
            employee=employee, start_date__range=(financial_year_start, today)
        ).count()

        leave_report.append({
            'employee': employee,
            'leaves_this_month': leaves_this_month,
            'leaves_this_quarter': leaves_this_quarter,
            'leaves_this_year': leaves_this_year,
            'total_sick': employee.total_sick,
            'total_earned': employee.total_earned,
        })

    context = {
        'leave_report': leave_report,
        'employees': employees,
        'total_employees': employees.count(),
        'total_active_employees': employees.filter(status='Active').count(),
        'total_inactive_employees': employees.filter(status='Inactive').count(),
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
def modify_employee(request, employee_id=None):
    if employee_id:
        employee = get_object_or_404(EmployeeProfile, id=employee_id)
    else:
        employee = None

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if not password.isdigit() or len(password) != 4:
                messages.error(request, "Password must be exactly 4 digits.")
                return render(request, "modify_employee.html", {"form": form})  # Re-render form with error
            else:
                form.save()
                messages.success(request, "Employee details saved successfully.")
                return redirect("admin_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, "modify_employee.html", {"form": form})  # Re-render with form errors
    else:
        form = EmployeeForm(instance=employee)

    return render(request, "modify_employee.html", {"form": form})
