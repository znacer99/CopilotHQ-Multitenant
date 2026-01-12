from django.http import HttpResponse
from django.db import connection
from tenants.models import Client
from django.conf import settings
import sys

class DomainTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hostname = request.get_host().split(':')[0]
        print(f"DEBUG: DomainTenantMiddleware processing hostname: {hostname}", file=sys.stderr)
        
        # Define the base domain
        base_domain = getattr(settings, 'TENANT_BASE_DOMAIN', 'copilothq.com')
        
        try:
            if hostname.endswith(f'.{base_domain}'):
                subdomain = hostname.replace(f'.{base_domain}', '')
                client = Client.objects.get(schema_name=subdomain)
                connection.set_tenant(client)
                request.tenant = client
                
            elif hostname.endswith('.localhost'):
                subdomain = hostname.replace('.localhost', '')
                client = Client.objects.get(schema_name=subdomain)
                connection.set_tenant(client)
                request.tenant = client
                
            elif hostname == base_domain or hostname == 'localhost' or hostname == '127.0.0.1':
                # For public, we MUST set the tenant object so connection.tenant is set
                try:
                    public_client = Client.objects.get(schema_name='public')
                    connection.set_tenant(public_client)
                    request.tenant = public_client
                except Client.DoesNotExist:
                    # Fallback to just schema if object missing (should not happen)
                    connection.set_schema('public')
                    request.tenant = None

            elif hostname == 'host.docker.internal':
                # Map docker internal requests to 'tenant1' tenant for dev
                client = Client.objects.get(schema_name='tenant1')
                connection.set_tenant(client)
                request.tenant = client
                print(f"DEBUG: Mapped host.docker.internal to tenant: {client.schema_name}", file=sys.stderr)
                
            else:
                # Handle other local dev hostnames if necessary (e.g. .local)
                if hostname.endswith('.local'):
                    subdomain = hostname.split('.')[0]
                    client = Client.objects.get(schema_name=subdomain)
                    connection.set_tenant(client)
                    request.tenant = client
                else:
                    # Fallback to public if no match? Or 404?
                    # Let's fallback to public to be safe, or just pass
                    # But if we pass without setting connection/tenant, django-tenants might be confused if strict.
                    # Let's treat as public.
                    connection.set_schema('public')
                    try:
                        public_client = Client.objects.get(schema_name='public')
                        request.tenant = public_client
                    except:
                        request.tenant = None

        except Client.DoesNotExist:
            print(f"DEBUG: Tenant not found for hostname: {hostname}", file=sys.stderr)
            return HttpResponse(f"Tenant not found for {hostname}", status=404)
        
        response = self.get_response(request)
        return response
