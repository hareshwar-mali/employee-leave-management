from rest_framework import routers
from django.urls import path, include, re_path

from .views import employee_login

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    re_path('login/', employee_login, name='login')
]
