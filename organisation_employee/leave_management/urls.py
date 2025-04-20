from django.urls import path
from .views import admin_dashboard, modify_employee, employee_login, employee_dashboard, apply_leave, home, admin_login

urlpatterns = [
    path('', home, name='home'),  # ⬅️ root URL will render your HTML homepage now
    path("home/", home, name="home"),
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),
    path("employee/add/", modify_employee, name="modify_employee"),
    path("employee/edit/<int:employee_id>/", modify_employee, name="modify_employee"),
    path("employee_login/", employee_login, name="employee_login"),
    path("admin_login/", admin_login, name="admin_login"),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('apply_leave/', apply_leave, name='apply_leave'),
]
