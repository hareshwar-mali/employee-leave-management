from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db.models import Count, Q
from django.contrib import messages
from .EmployeeForm import EmployeeForm
from .LeaveApplicationForm import LeaveApplicationForm
from .models import EmployeeProfile, EmployeeLeave
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.utils import timezone


def home(request):
    return render(request, 'index.html')


def admin_login(request):
    error = None
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        try:
            # Get the employee based on the phone number
            employee = EmployeeProfile.objects.get(phone_number=phone_number)

            # Ensure the employee is an admin
            if not employee.user.is_staff:
                error = 'You do not have permission to perform this action.'
                return render(request, 'admin_login.html', {'error': error})

            # If user is admin, verify password
            if password == employee.password:
                request.session['employee_id'] = employee.id
                request.session['employee_name'] = f"{employee.first_name} {employee.last_name}"
                request.session['employee_phone'] = employee.phone_number  # Store phone number
                login(request, employee.user)  # Log in the user using Django's auth system
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                error = 'Invalid password.'
        except EmployeeProfile.DoesNotExist:
            error = 'Employee not found.'

    return render(request, 'admin_login.html', {'error': error})


@login_required
def admin_dashboard(request):
    today = now().date()
    first_day_of_month = today.replace(day=1)
    # Consider three months of quarter
    current_quarter = (today.month - 1) // 3 + 1
    first_day_of_quarter = datetime(today.year, 3 * current_quarter - 2, 1).date()
    # Consider financial year start from 1 Apr
    financial_year_start = datetime(today.year if today.month >= 4 else today.year - 1, 4, 1).date()

    employee_queryset = EmployeeProfile.objects.all()
    employees = employee_queryset.annotate(
        total_sick=Count('employeeleave', filter=Q(employeeleave__leave_type='CS')),
        total_earned=Count('employeeleave', filter=Q(employeeleave__leave_type='E')),
        leaves_this_month=Count('employeeleave',
                                filter=Q(employeeleave__start_date__range=(first_day_of_month, today))),
        leaves_this_quarter=Count('employeeleave',
                                  filter=Q(employeeleave__start_date__range=(first_day_of_quarter, today))),
        leaves_this_year=Count('employeeleave',
                               filter=Q(employeeleave__start_date__range=(financial_year_start, today)))
    ).order_by('id')

    leave_report = []
    for employee in employees:
        leave_report.append({
            'employee': employee,
            'leaves_this_month': employee.leaves_this_month,
            'leaves_this_quarter': employee.leaves_this_quarter,
            'leaves_this_year': employee.leaves_this_year,
            'total_sick': employee.total_sick,
            'total_earned': employee.total_earned,
        })

    context = {
        'leave_report': leave_report,
        'employees': employees,
        'total_employees': employee_queryset.count(),
        'total_active_employees': employee_queryset.filter(status='Active').count(),
        'total_inactive_employees': employee_queryset.filter(status='Inactive').count(),
    }

    return render(request, 'admin_dashboard.html', context)


def employee_login(request):
    error = None
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
                error = 'Invalid password.'
        except EmployeeProfile.DoesNotExist:
            error = 'Employee not found.'

    return render(request, 'login.html', {'error': error})


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
            leave_days = (leave.end_date - leave.start_date).days
            if leave.leave_type == 'CS':
                employee.total_cs_leaves = employee.total_cs_leaves - leave_days
            else:
                employee.total_e_leaves = employee.total_e_leaves - leave_days
            employee.save()
            return redirect('employee_dashboard')
    else:
        form = LeaveApplicationForm()

    return render(request, 'apply_leave.html', {'form': form})
