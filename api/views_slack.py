import os
import logging
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from agents.orchestrator import OrchestratorAgent
from employees.models import Employee
from django.db import connection

logger = logging.getLogger(__name__)

# Initialize Slack App (with fallback to prevent server crash if keys are missing)
bot_token = os.environ.get("SLACK_BOT_TOKEN")
signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

if bot_token and bot_token.startswith("xoxb-") and signing_secret:
    try:
        app = App(
            token=bot_token,
            signing_secret=signing_secret
        )
    except Exception:
        # If it still fails (e.g. invalid token), use a dummy
        class DummyApp:
            def event(self, *args, **kwargs): return lambda f: f
        app = DummyApp()
else:
    class DummyApp:
        def event(self, *args, **kwargs): return lambda f: f
    app = DummyApp()
    logger.warning("Slack Integration is DISABLED (missing or invalid tokens).")

@app.event("message")
def handle_message(event, say):
    """Router for all Slack messages"""
    user_id = event.get("user")
    text = event.get("text")
    channel = event.get("channel")
    
    if event.get("subtype") == "bot_message":
        return

    # 1. Identify Employee & Tenant
    # In production, we'd map Slack user_id to our Employee model
    try:
        # Mocking tenant identification for now
        from tenants.models import Client
        tenant = Client.objects.exclude(schema_name='public').first()
        
        with connection.tenant_context(tenant):
            employee = Employee.objects.first() # Mocking the user
            
            # 2. Call Orchestrator
            agent = OrchestratorAgent(tenant)
            response = agent.handle_request(text)
            
            # 3. Format Response
            if "summary" in response:
                summary = response["summary"]
                say(f"🧠 *Orchestrator*: {summary}")
            elif "message" in response:
                say(f"🤖 *Agent*: {response['message']}")
            elif "plan" in response:
                steps = "\n".join([f"{p['step']}. {p['agent']}: {p['action']}" for p in response["plan"]])
                say(f"🚀 *Action Plan*:\n{steps}")
            else:
                say("I've received your request and am processing it.")
                
    except Exception as e:
        logger.error(f"Slack Handler Error: {str(e)}")
        say("Sorry, I encountered an internal error processing that request.")

# Django View to handle requests from Slack
if hasattr(app, 'name'): # Real Bolt App has a name/client
    handler = SlackRequestHandler(app)
else:
    handler = None

@csrf_exempt
def slack_events_endpoint(request: HttpRequest):
    if handler:
        return handler.handle(request)
    return HttpResponse("Slack integration is not configured on this server.", status=503)
