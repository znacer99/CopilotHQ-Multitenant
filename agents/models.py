from django.db import models
from django.conf import settings
from tenants.models import Client

class AgentConfig(models.Model):
    """Configuration for tenant's AI agents"""
    tenant = models.OneToOneField(Client, on_delete=models.CASCADE)
    enabled_agents = models.JSONField(default=list)  # ['support', 'recruiting']
    agent_settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'agents'

class AgentLog(models.Model):
    """Audit trail for agent actions"""
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent_type = models.CharField(max_length=50)
    action = models.CharField(max_length=100)
    prompt = models.TextField(blank=True)
    response = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'agents'
        indexes = [
            models.Index(fields=['tenant', 'created_at']),
            models.Index(fields=['agent_type']),
        ]

class AgentTask(models.Model):
    """Async tasks for agents"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent_type = models.CharField(max_length=50)
    task_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    input_data = models.JSONField()
    output_data = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        app_label = 'agents'

class KnowledgeBase(models.Model):
    """Knowledge base for agents to draw information from"""
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()  # Extracted text
    source_file = models.FileField(upload_to='kb_docs/', null=True, blank=True)
    category = models.CharField(max_length=100, default='General')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.tenant.schema_name})"
    
    class Meta:
        app_label = 'agents'

class ConversationHistory(models.Model):
    """Chat history between employees and support agent"""
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    messages = models.JSONField(default=list)  # [{"role": "user", "content": "..."}]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'agents'
