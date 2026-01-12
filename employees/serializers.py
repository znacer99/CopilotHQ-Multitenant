from rest_framework import serializers
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'department', 'department_name', 'position', 
            'salary', 'contract_type', 'hire_date', 'status', 
            'national_id', 'address', 'phone', 
            'emergency_contact_name', 'emergency_contact_phone', 
            'profile_photo', 'created_at'
        ]

class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new employees with a user account."""
    email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Employee
        fields = ['email', 'position', 'department', 'hire_date', 'status', 'contract_type']
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        # Create or get user
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password('changeme123')  # Default password
            user.save()
        # Create employee
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
