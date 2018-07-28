from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib import staticfiles

def index(request):
    response = TemplateResponse(request, 'index.html', {})
    return response

def calEquity(request):
    return HttpResponse("success")
