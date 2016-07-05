from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
# from django.http import HttpResponseRedirect

from .models_l_env454 import Run
from .forms import RunForm
from .utils import get_run


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

# def detail(request, run_id):
#     return HttpResponse("You're looking at run %s." % run_id)
#
# def detail(request, run_id):
#     try:
#         run = Run.objects.get(pk=run_id)
#     except Run.DoesNotExist:
#         raise Http404("Run does not exist")
#     return render(request, 'submission/detail.html', {'run': run})


def detail(request, run_id):
    run = get_object_or_404(Run, pk=run_id)
    return render(request, 'submission/detail.html', {'run': run})


def results(request, run_id):
    response = "You're looking at the results of run %s."
    return HttpResponse(response % run_id)


def vote(request, run_id):
    return HttpResponse("You're voting on run %s." % run_id)


def help(request):
    return render(request, 'submission/help.html')

def db_upload(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
    except:
        form = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Data upload to db', 'is_cluster': 'not', 'pipeline_command': 'env454upload' })

def run_info_upload(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
    except:
        form = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Run info upload to db', 'is_cluster': 'not', 'pipeline_command': 'env454run_info_upload' })

def chimera_checking(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
    except:
        form = get_run(request)
    return render(request, 'submission/chimera_checking.html', {'form': form, 'run_data': run_data, 'header': 'Chimera checking (for v4v5 region only)', 'is_cluster': '', 'pipeline_command': 'illumina_chimera_only' })

def demultiplex(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
    except:
        form = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Demultiplex Illumina files by index/run_key/lane', 'is_cluster': 'not', 'pipeline_command': 'illumina_files_demultiplex_only' })

def overlap(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
    except:
        form = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap, filter and unique reads in already demultiplexed files', 'is_cluster': '', 'pipeline_command': 'illumina_files' })
    
def gast(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
        # print "!!!form.cleaned_data"
        # print form.cleaned_data
        # print "555 find_rundate = "
        # print run_data['find_rundate']
    except:
        form = get_run(request)
    return render(request, 'submission/gast.html', {'form': form, 'run_data': run_data, 'header': 'Gast', 'is_cluster': 'not'})

def gzip_all(request):
    run_data = {}
    try:
        form, run_data = get_run(request)
    except:
        form = get_run(request)
    return render(request, 'submission/gzip_all.html', {'form': form, 'run_data': run_data, 'header': 'Gzip all files', 'is_cluster': 'not', 'menu_name': 'gast'})

