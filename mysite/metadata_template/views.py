from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the metadata_template index.")
    
def metadata_form(request):
    return render(request, 'metadata_template/metadata_form.html', {})
    
