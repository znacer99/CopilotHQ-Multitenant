from celery import shared_task
from django.db import connection
from tenants.models import Client
from .support import SupportAgent
from .recruiting import RecruitingAgent
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_agent_task(tenant_id, agent_type, task_type, input_data):
    """Generic background task for AI agents"""
    try:
        tenant = Client.objects.get(id=tenant_id)
        connection.set_tenant(tenant)
        
        if agent_type == 'support':
            # Example: Process a complex support query in background
            pass
        elif agent_type == 'recruiting':
            # Example: Bulk screen candidates
            pass
            
        logger.info(f"Successfully processed {agent_type} task for tenant {tenant.name}")
        
    except Exception as e:
        logger.error(f"Error processing agent task: {str(e)}")
        raise

@shared_task
def trigger_n8n_webhook(webhook_url, payload):
    """Task to trigger an external n8n workflow"""
    import requests
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully triggered n8n webhook: {webhook_url}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to trigger n8n webhook: {str(e)}")
        return {"error": str(e)}
