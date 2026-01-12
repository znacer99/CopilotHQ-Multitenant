import anthropic
from django.db import connection
from django.conf import settings
from .models import AgentLog
import json
import logging

logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base class for all AI agents
    Each agent is tenant-aware and isolated
    """
    
    agent_type = "base"
    
    def __init__(self, tenant):
        self.tenant = tenant
        self.api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
        
        if self.api_key and self.api_key != 'your-key-here':
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.mock_mode = False
        else:
            self.client = None
            self.mock_mode = True
            logger.warning(f"Starting {self.agent_type} agent in MOCK MODE (API key missing)")
            
        self.context = self.build_context()
        
    def build_context(self):
        """
        Build tenant-specific context
        Override in subclasses to add specialized context
        """
        connection.set_tenant(self.tenant)
        
        # Import models inside to avoid circular imports if any
        from employees.models import Employee
        from departments.models import Department
        
        context = f"""You are an AI agent for {self.tenant.name}.

CRITICAL RULES:
1. You can ONLY access data for {self.tenant.name}
2. Never reference or use data from other companies
3. All data is tenant-isolated in schema: {self.tenant.schema_name}

COMPANY INFORMATION:
- Company Name: {self.tenant.name}
- Total Employees: {Employee.objects.count()}
- Departments: {list(Department.objects.values_list('name', flat=True))}
- Your permissions: {self.get_permissions()}

POLICIES:
{self.get_company_policies()}
"""
        return context
    
    def get_permissions(self):
        """Override in subclasses"""
        return []
    
    def get_company_policies(self):
        """Fetch company policies from database"""
        # TODO: Implement policy model or fetch from a known location
        return "Standard HR policies apply."
    
    def call_claude(self, user_message, tools=None, max_tokens=4000):
        """
        Make API call to Claude with tenant context or return mock response
        """
        if self.mock_mode:
            return self._mock_call_claude(user_message, tools)

        messages = [
            {
                "role": "user",
                "content": f"[TENANT: {self.tenant.schema_name}]\n\n{user_message}"
            }
        ]
        
        try:
            response = self.client.messages.create(
                model=getattr(settings, 'AGENT_SETTINGS', {}).get('MODEL', 'claude-3-5-sonnet-20240620'),
                max_tokens=max_tokens,
                system=self.context,
                messages=messages,
                tools=tools or []
            )
            
            # Log the interaction
            self.log_interaction(user_message, response)
            
            return response
            
        except Exception as e:
            self.log_error(str(e))
            raise

    def _mock_call_claude(self, user_message, tools=None):
        """Simulate Claude response for development"""
        logger.info(f"MOCK AI CALL: {user_message[:100]}...")
        
        # Simple rule-based mock responses for demo/dev
        mock_text = f"This is a MOCK response from the {self.agent_type} agent. I've received your message: '{user_message[:50]}...'. In a production environment with an API key, I would provide a real answer using the tenant context for {self.tenant.name}."
        
        class MockUsage:
            def __init__(self):
                self.input_tokens = 0
                self.output_tokens = 0

        class MockContentBlock:
            def __init__(self, text):
                self.text = text
                self.type = "text"

        class MockResponse:
            def __init__(self, text):
                self.content = [MockContentBlock(text)]
                self.model = "mock-model"
                self.usage = MockUsage()

        # Log the mock interaction
        self.log_interaction(user_message, MockResponse(mock_text))
        return MockResponse(mock_text)
    
    def log_interaction(self, prompt, response):
        """Log agent interactions for audit trail"""
        connection.set_tenant(self.tenant)
        
        # Check if response content is a list or object
        try:
            if hasattr(response.content[0], 'text'):
                resp_text = response.content[0].text
            else:
                resp_text = str(response.content)
        except:
            resp_text = str(response)

        AgentLog.objects.create(
            tenant=self.tenant,
            agent_type=self.agent_type,
            action="call_claude",
            prompt=prompt[:5000],
            response=resp_text[:5000],
            metadata={
                "model": getattr(response, 'model', 'unknown'),
                "usage": {
                    "input_tokens": getattr(response.usage, 'input_tokens', 0),
                    "output_tokens": getattr(response.usage, 'output_tokens', 0),
                } if hasattr(response, 'usage') else {}
            }
        )
    
    def log_error(self, error):
        """Log errors"""
        connection.set_tenant(self.tenant)
        
        AgentLog.objects.create(
            tenant=self.tenant,
            agent_type=self.agent_type,
            action="error",
            response=error,
        )
    
    def extract_text_response(self, response):
        """Extract text from Claude response"""
        text_blocks = [
            block.text for block in response.content 
            if hasattr(block, 'text')
        ]
        return "\n".join(text_blocks)
