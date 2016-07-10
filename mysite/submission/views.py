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
    return render(request, 'submission/help.html', {'header': 'Help and tips'})

def metadata_upload(request):
    return render(request, 'submission/metadata_upload.html', {'header': 'Upload submission metadata'})

def data_upload(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Data upload to db', 'is_cluster': 'not', 'pipeline_command': 'env454upload',  'error_message': error_message})

def run_info_upload(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Run info upload to db', 'is_cluster': 'not', 'pipeline_command': 'env454run_info_upload',  'error_message': error_message })

def chimera_checking(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Chimera checking (for v4v5 region only)', 'is_cluster': '', 'pipeline_command': 'illumina_chimera_only', 'what_to_check': 'statistics ', 'check_command': 'chimera/; chimera_stats.py', 'error_message': error_message})

def demultiplex(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Demultiplex Illumina files by index/run_key/lane', 'is_cluster': 'not', 'pipeline_command': 'illumina_files_demultiplex_only',  'error_message': error_message })

def overlap(request):
    run_data = {}
    check_command = ''
    try:
        form, run_data, error_message = get_run(request)
        check_command = 'reads_overlap/; take_%s_stats.py' % run_data['find_machine']
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap, filter and unique reads in already demultiplexed files', 'is_cluster': '', 'pipeline_command': 'illumina_files', 'what_to_check': 'the overlap percentage ', 'check_command': check_command, 'error_message': error_message })

def overlap_only(request):
    run_data = {}
    check_command = ''
    try:
        form, run_data, error_message = get_run(request)
        check_command = 'reads_overlap/; take_%s_stats.py' % run_data['find_machine']
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap reads in already demultiplexed files', 'is_cluster': '', 'command': '; run_partial_overlap_clust.sh; date', 'what_to_check': 'the overlap percentage ', 'check_command': check_command, 'error_message': error_message })


def filter_mismatch(request):
    run_data = {}
    header = '''Filtering partial (Ev4, v4v5 and ITS1) merged\n
    Maximum number of mismatches allowed in the overlapped region is 3'''
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': header, 'is_cluster': '', 'command': 'reads_overlap/; run_mismatch_filter.sh; date',  'error_message': error_message })
    
def gast(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
        # print "!!!form.cleaned_data"
        # print form.cleaned_data
        # print "555 find_rundate = "
        # print run_data['find_rundate']
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gast', 'is_cluster': 'not', 'command': 'reads_overlap/; run_gast_ill_nonchim_sge.sh; date', 'what_to_check': 'the percent of "Unknown" taxa ', 'check_command': 'gast/; percent10_gast_unknowns.sh', 'error_message': error_message})

def gzip_all(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gzip all files', 'is_cluster': 'not', 'command': '; time gzip -r *',  'error_message': error_message})

def clear_db(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/clear_db.html', {'form': form, 'run_data': run_data, 'header': 'Remove old data from db',  'error_message': error_message})

def uniqueing(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Uniqueing fasta files', 'is_cluster': '', 'command': 'reads_overlap/; run_unique_fa.sh; date',  'error_message': error_message })

def check_fa_counts(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Check counts in fasta files', 'is_cluster': 'not', 'command': 'reads_overlap/; grep '>' *REMOVED.unique | wc -l; date',  'error_message': error_message})

def check_db_counts(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/check_db_counts.html', {'form': form, 'run_data': run_data, 'header': 'Check counts in db', 'error_message': error_message})

def gunzip_all(request):
    run_data = {}
    try:
        form, run_data, error_message = get_run(request)
    except:
        form, error_message = get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gunzip all files', 'is_cluster': 'not', 'command': '; time gunzip -r *.gz',  'error_message': error_message})