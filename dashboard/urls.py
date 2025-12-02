from django.urls import path
from .views import tenant_home

urlpatterns = [
    path('', tenant_home),
]
