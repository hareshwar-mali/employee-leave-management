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
from django.utils import timezone
from django.contrib.auth import logout


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


@login_required()
def employee_login(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        try:
            employee = EmployeeProfile.objects.get(phone_number=phone_number)
            if employee.password == password:
                request.session['employee_id'] = employee.id
                request.session['employee_name'] = f"{employee.first_name} {employee.last_name}"
                request.session['employee_phone'] = employee.phone_number  # Store phone number
                return redirect('employee_dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except EmployeeProfile.DoesNotExist:
            messages.error(request, 'Employee not found.')
    return render(request, 'login.html')


# Employee Dashboard to show leave balance and leave applied
@login_required
def employee_dashboard(request):
    phone_number = request.session.get('employee_phone')
    if not phone_number:
        messages.error(request, "Session expired or invalid access. Please login again.")
        return redirect('login')

    employee = get_object_or_404(EmployeeProfile, phone_number=phone_number)

    # Calculate leaves taken
    current_date = timezone.now()
    current_month = current_date.month
    current_quarter = (current_date.month - 1) // 3 + 1
    current_year = current_date.year

    leaves_this_month = EmployeeLeave.objects.filter(employee=employee, start_date__month=current_month)
    leaves_this_quarter = EmployeeLeave.objects.filter(employee=employee, start_date__quarter=current_quarter)
    leaves_this_year = EmployeeLeave.objects.filter(employee=employee, start_date__year=current_year)

    leave_balance = {
        'sick': employee.total_cs_leaves,
        'earned': employee.total_e_leaves,
        'month': leaves_this_month.count(),
        'quarter': leaves_this_quarter.count(),
        'year': leaves_this_year.count(),
    }

    return render(request, 'employee_dashboard.html', {
        'employee': employee,
        'leave_balance': leave_balance,
        'leaves_taken': leaves_this_month,
    })



@login_required
def apply_leave(request):
    phone_number = request.session.get('employee_phone')
    employee = get_object_or_404(EmployeeProfile, phone_number=phone_number)

    if request.method == "POST":
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.save()
            messages.success(request, "Leave applied successfully.")
            return redirect('employee_dashboard')
    else:
        form = LeaveApplicationForm()

    return render(request, 'apply_leave.html', {'form': form})


def employee_logout(request):
    logout(request)
    return redirect('employee_login')  # Redirect to login after logout