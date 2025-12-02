from django.urls import path
from common.views import public_home

urlpatterns = [
    path("", public_home, name="public_home"),
]
