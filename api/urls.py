from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_agents import (
    support_chat, support_history,
    recruiting_source, recruiting_screen,
    onboarding_plan, payroll_pto,
    knowledge_search, knowledge_ingest, analytics_stats,
    orchestrator_run,
    trigger_workflow
)
from .views import tenant_info
from employees.views import EmployeeViewSet
from candidates.views import CandidateViewSet, JobViewSet
from leave.views import LeaveRequestViewSet, LeaveBalanceViewSet
from . import views_slack

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register(r'leave-balances', LeaveBalanceViewSet, basename='leave-balance')

urlpatterns = [
    # Router endpoints (Employees, etc)
    path('', include(router.urls)),
    
    # Tenant info endpoint
    path('tenant/', tenant_info, name='tenant_info'),

    # Agent endpoints
    path('agents/support/chat/', support_chat, name='support_chat'),
    path('agents/support/history/', support_history, name='support_history'),
    path('agents/recruiting/source/', recruiting_source, name='recruiting_source'),
    path('agents/recruiting/screen/', recruiting_screen, name='recruiting_screen'),
    path('agents/onboarding/plan/', onboarding_plan, name='onboarding_plan'),
    path('agents/payroll/pto/', payroll_pto, name='payroll_pto'),
    path('agents/knowledge/search/', knowledge_search, name='knowledge_search'),
    path('agents/knowledge/ingest/', knowledge_ingest, name='knowledge_ingest'),
    path('agents/analytics/stats/', analytics_stats, name='analytics_stats'),
    path('agents/orchestrator/run/', orchestrator_run, name='orchestrator_run'),
    path('agents/workflow/trigger/', trigger_workflow, name='trigger_workflow'),
    
    # Slack Integration
    path('slack/events/', views_slack.slack_events_endpoint, name='slack_events'),
]
