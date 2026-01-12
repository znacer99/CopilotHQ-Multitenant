from django.contrib import admin
from django.urls import path
from common.views import public_home
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", public_home, name="public_home"),
    path("admin/", admin.site.urls),
    path("api/auth/login/", obtain_auth_token, name="api_token_auth"),
]
