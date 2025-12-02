from django.contrib import admin
from django.urls import path, include
from common.views import tenant_home

urlpatterns = [
    path("", tenant_home),   # tenant homepage
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("accounts/", include("accounts.urls")),
    path("employees/", include("employees.urls")),
    path("departments/", include("departments.urls")),
    path("documents/", include("documents.urls")),
    path("leave/", include("leave.urls")),
    path("candidates/", include("candidates.urls")),
    path("dashboard/", include("dashboard.urls")),
]
