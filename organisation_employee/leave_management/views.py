from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .LeaveApplicationForm import LeaveApplicationForm
from .models import EmployeeProfile, EmployeeLeave
from django.contrib.auth.decorators import login_required


def employee_login(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        try:
            employee = EmployeeProfile.objects.get(phone_number=phone_number)
            if employee.password == password:
                # Manually create session for employee
                request.session['employee_id'] = employee.id
                request.session['employee_name'] = f"{employee.first_name} {employee.last_name}"
                return redirect('login')
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except EmployeeProfile.DoesNotExist:
            return render(request, 'login.html', {'error': 'Employee not found'})
    return render(request, 'login.html')
