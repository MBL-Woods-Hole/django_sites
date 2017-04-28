from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    
def metadata_form(request):
    return render(request, 'metadata_template/metadata_form.html', {})
    
    """
    django.template.loaders.app_directories.Loader: /Users/ashipunova/BPC/python_web/django_sites/mysite/submission/templates/metadata_template/metadata_form.html (Source does not exist)
    
    """
    
