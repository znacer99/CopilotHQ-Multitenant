from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.conf import settings

from tenants.models import Client

def public_home(request):
    # Fetch all tenants (excluding the public one itself)
    tenants = Client.objects.exclude(schema_name='public')
    base_domain = getattr(settings, 'TENANT_BASE_DOMAIN', 'copilothq.com')
    return render(request, 'public/index.html', {
        'tenants': tenants,
        'base_domain': base_domain
    })

@login_required
def tenant_home(request):
    tenant = connection.tenant
    return render(request, 'playground/playground.html', {'tenant': tenant})
