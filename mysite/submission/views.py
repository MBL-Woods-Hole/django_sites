
'''
# from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Illumina files processing")
    
# def 
'''
#
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.views.generic import TemplateView
#
# def index(request):
#   return render_to_response('submission/index.html', context_instance=RequestContext(request))
#
#
# class HelpView(TemplateView):
#     template_name = "help.html"
#
# from django.http import HttpResponse
#
# def index(request):
#     return HttpResponse("Illumina files processing")
#
# from django.http import HttpResponse
#
# from .models_l_env454 import Run
#
# def index(request):
#     latest_run_list = Run.objects.order_by('-run')[:10]
#     output = ', '.join([q.run for q in latest_run_list])
#     return HttpResponse(output)

from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render
from .models_l_env454 import Run


# def index(request):
#     latest_run_list = Run.objects.order_by('-run')[:15]
#     template = loader.get_template('submission/index.html')
#     context = {
#         'latest_run_list': latest_run_list,
#     }
#     return HttpResponse(template.render(context, request))


def index(request):
    latest_run_list = Run.objects.order_by('-run')[:10]
    context = {'latest_run_list': latest_run_list}
    return render(request, 'submission/index.html', context)
        
def detail(request, run_id):
    return HttpResponse("You're looking at run %s." % run_id)

def results(request, run_id):
    response = "You're looking at the results of run %s."
    return HttpResponse(response % run_id)

def vote(request, run_id):
    return HttpResponse("You're voting on run %s." % run_id)