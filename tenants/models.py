from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# Tenant = the company account
class Client(TenantMixin):
    name = models.CharField(max_length=255)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # required by django-tenants
    auto_create_schema = True

    def __str__(self):
        return self.name


# Domain = the URL assigned to a tenant
class Domain(DomainMixin):
    pass
