import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CopilotHQ.settings.base')
django.setup()

from tenants.models import Client, Domain
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_data():
    # Create public tenant if it doesn't exist
    public_tenant, created = Client.objects.get_or_create(
        schema_name='public',
        name='Public'
    )
    if created:
        Domain.objects.create(domain='copilothq.com', tenant=public_tenant, is_primary=True)

    # Create test tenant
    tenant, created = Client.objects.get_or_create(
        schema_name='tenant1',
        name='Test Company 1'
    )
    if created:
        Domain.objects.create(domain='tenant1.copilothq.com', tenant=tenant, is_primary=True)
        print(f"Created tenant: {tenant.name}")

    # Create superuser in public
    if not User.objects.filter(email='admin@copilothq.com').exists():
        User.objects.create_superuser('admin@copilothq.com', 'password123')
        print("Created superuser admin@copilothq.com / password123")

if __name__ == "__main__":
    create_test_data()
