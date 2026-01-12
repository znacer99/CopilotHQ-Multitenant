from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

from agents.support import SupportAgent
from agents.models import ConversationHistory

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def support_chat(request):
    """
    Endpoint for employees to chat with support agent
    
    POST /api/agents/support/chat/
    {
        "message": "How many vacation days do I have?"
    }
    """
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)
        
    employee = request.user
    message = request.data.get('message')
    
    if not message:
        return Response(
            {"error": "message is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        agent = SupportAgent(tenant)
        result = agent.answer_question(employee, message)
        
        return Response({
            "success": True,
            "answer": result["answer"],
            "tool_calls": result.get("tool_calls", []),
            "conversation_id": result["conversation_id"]
        })
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def support_history(request):
    """
    Get conversation history
    
    GET /api/agents/support/history/
    """
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    employee = request.user
    
    try:
        conversation = ConversationHistory.objects.get(
            tenant=tenant,
            employee=employee
        )
        
        return Response({
            "messages": conversation.messages,
            "updated_at": conversation.updated_at
        })
        
    except ConversationHistory.DoesNotExist:
        return Response({"messages": []})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recruiting_source(request):
    """
    POST /api/agents/recruiting/source/
    {
        "job_id": 123
    }
    """
    from agents.recruiting import RecruitingAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    job_id = request.data.get('job_id')
    if not job_id:
        return Response({"error": "job_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    agent = RecruitingAgent(tenant)
    strategies = agent.source_candidates(job_id)
    
    return Response(strategies)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recruiting_screen(request):
    """
    POST /api/agents/recruiting/screen/
    {
        "candidate_id": 456,
        "job_id": 123
    }
    """
    from agents.recruiting import RecruitingAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    candidate_id = request.data.get('candidate_id')
    job_id = request.data.get('job_id')
    
    if not candidate_id or not job_id:
        return Response({"error": "candidate_id and job_id are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    agent = RecruitingAgent(tenant)
    evaluation = agent.screen_resume(candidate_id, job_id)
    
    return Response(evaluation)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def onboarding_plan(request):
    """
    POST /api/agents/onboarding/plan/
    {
        "employee_id": 1
    }
    """
    from agents.onboarding import OnboardingAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    employee_id = request.data.get('employee_id')
    if not employee_id:
        return Response({"error": "employee_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    agent = OnboardingAgent(tenant)
    plan = agent.generate_plan(employee_id)
    
    return Response(plan)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payroll_pto(request):
    """
    POST /api/agents/payroll/pto/
    {
        "employee_id": 1
    }
    """
    from agents.payroll import PayrollAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    employee_id = request.data.get('employee_id')
    if not employee_id:
        return Response({"error": "employee_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    agent = PayrollAgent(tenant)
    summary = agent.get_pto_summary(employee_id)
    
    return Response(summary)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def knowledge_search(request):
    """
    POST /api/agents/knowledge/search/
    {
        "query": "What is the remote work policy?"
    }
    """
    from agents.knowledge import KnowledgeAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    query = request.data.get('query')
    if not query:
        return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    agent = KnowledgeAgent(tenant)
    results = agent.search_knowledge(query)
    
    return Response(results)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def knowledge_ingest(request):
    """
    POST /api/agents/knowledge/ingest/
    {
        "title": "Remote Work Policy",
        "content": "Employees can work from home..."
    }
    """
    from agents.knowledge import KnowledgeAgent
    from agents.models import KnowledgeBase
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    title = request.data.get('title')
    content = request.data.get('content')
    
    if not title or not content:
        return Response({"error": "title and content are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Save directly to database
    kb_entry, created = KnowledgeBase.objects.update_or_create(
        tenant=tenant,
        title=title,
        defaults={'content': content, 'category': 'Manual'}
    )
    
    return Response({"success": True, "created": created, "title": title})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_stats(request):
    """
    GET /api/agents/analytics/stats/
    """
    from agents.analytics import AnalyticsAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    agent = AnalyticsAgent(tenant)
    stats = agent.get_dashboard_stats()
    
    return Response(stats)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orchestrator_run(request):
    """
    POST /api/agents/orchestrator/run/
    {
        "query": "Help me hire a new dev and plan their onboarding"
    }
    """
    from agents.orchestrator import OrchestratorAgent
    
    tenant = getattr(connection, 'tenant', None)
    if not tenant:
        return Response({"error": "Tenant not identified"}, status=status.HTTP_400_BAD_REQUEST)

    query = request.data.get('query')
    if not query:
        return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    agent = OrchestratorAgent(tenant)
    plan = agent.handle_request(query)
    
    return Response(plan)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_workflow(request):
    """
    POST /api/agents/workflow/trigger/
    {
        "workflow_id": "...",
        "data": {...}
    }
    """
    from agents.tasks import trigger_n8n_webhook
    
    webhook_url = request.data.get('webhook_url')  # In production, fetch from settings/db
    payload = request.data.get('data', {})
    
    if not webhook_url:
        return Response({"error": "webhook_url is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Trigger via Celery to keep request fast
    trigger_n8n_webhook.delay(webhook_url, payload)
    
    return Response({"success": True, "message": "Workflow triggered in background"})
