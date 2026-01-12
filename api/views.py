from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tenant_info(request):
    """Return current tenant information for the frontend."""
    tenant = getattr(request, 'tenant', None)
    if tenant:
        return Response({
            'name': tenant.name,
            'schema_name': tenant.schema_name,
        })
    return Response({'name': 'Unknown', 'schema_name': 'public'})
