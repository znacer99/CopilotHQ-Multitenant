from django.test import TestCase
from django.db import connection
from tenants.models import Client
from employees.models import Employee
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class TenantIsolationTest(TestCase):
    def setUp(self):
        # Ensure we are in public schema to create tenants
        connection.set_schema_to_public()
        
        self.tenant1 = Client.objects.create(
            schema_name='test_tenant1',
            name='Test Company 1'
        )
        self.tenant2 = Client.objects.create(
            schema_name='test_tenant2',
            name='Test Company 2'
        )
        
    def test_data_isolation(self):
        # Create employee in tenant1
        connection.set_tenant(self.tenant1)
        user1 = User.objects.create_user(username="alice", password="password123")
        Employee.objects.create(user=user1, position="Manager", hire_date=date.today())
        
        self.assertEqual(Employee.objects.count(), 1)
        
        # Switch to tenant2
        connection.set_tenant(self.tenant2)
        
        # Verify tenant2 can't see tenant1's data
        self.assertEqual(Employee.objects.count(), 0)
        
    def test_schema_switching(self):
        connection.set_tenant(self.tenant1)
        self.assertEqual(connection.schema_name, 'test_tenant1')
        
        connection.set_tenant(self.tenant2)
        self.assertEqual(connection.schema_name, 'test_tenant2')
