from rest_framework import routers
from django.urls import path, include, re_path

from .views import admin_dashboard, modify_employee

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),
    path("employee/add/", modify_employee, name="modify_employee"),
    path("employee/edit/<int:employee_id>/", modify_employee, name="modify_employee"),
]
