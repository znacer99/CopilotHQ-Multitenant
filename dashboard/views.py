from django.http import HttpResponse

def tenant_home(request):
    return HttpResponse("TENANT SCHEMA — OK")
