import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CopilotHQ.settings.base")
django.setup()

from tenants.models import Client, Domain
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

def create_tenant(name, schema_name, domain_url):
    tenant, created = Client.objects.get_or_create(
        schema_name=schema_name,
        defaults={'name': name}
    )
    if created:
        print(f"✅ Created tenant '{name}' ({schema_name})")
    else:
        print(f"ℹ️ Tenant '{name}' already exists.")

    # Create Domain
    domain, created = Domain.objects.get_or_create(
        domain=domain_url,
        tenant=tenant,
        defaults={'is_primary': True}
    )
    if created:
        print(f"✅ Created domain '{domain_url}'")
    
    return tenant

def create_admin_user(tenant, email, password="password"):
    connection.set_tenant(tenant)
    print(f"Creating admin for {tenant.schema_name}...")
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'is_staff': True, 'is_superuser': True}
    )
    user.set_password(password)
    user.save()
    
    # Create Employee Profile for testing
    from employees.models import Employee
    from departments.models import Department
    
    # Ensure HR dept exists
    dept, _ = Department.objects.get_or_create(name="HR", defaults={'description': "Human Resources"})
    
    Employee.objects.get_or_create(
        user=user,
        defaults={
            'position': 'Admin',
            'department': dept,
            'hire_date': '2024-01-01',
            'status': 'active'
        }
    )

    print(f"✅ Admin user '{email}' ready for {tenant.schema_name}")

if __name__ == "__main__":
    print("--- Setting up Multi-tenant Environment ---")
    
    # Tenant 1 (Acme Corp)
    t1 = create_tenant("Acme Corp", "tenant1", "tenant1.localhost")
    create_admin_user(t1, "admin@acme.com")
    
    # Switch back to public schema to create next tenant
    connection.set_schema_to_public()

    # Tenant 2 (Globex Inc)
    t2 = create_tenant("Globex Inc", "tenant2", "tenant2.localhost")
    create_admin_user(t2, "admin@globex.com")
    
    print("\n--- Setup Complete ---")
    print("Add these to your /etc/hosts:")
    print("127.0.0.1 tenant1.localhost")
    print("127.0.0.1 tenant2.localhost")
