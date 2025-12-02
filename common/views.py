from django.http import HttpResponse

def public_home(request):
    return HttpResponse("PUBLIC SCHEMA — OK")

def tenant_home(request):
    return HttpResponse(f"TENANT SCHEMA — OK")
