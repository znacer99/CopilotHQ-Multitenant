import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CopilotHQ.settings.base')
django.setup()

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email='admin@copilothq.com')
token, created = Token.objects.get_or_create(user=user)
print(f"TOKEN: {token.key}")
