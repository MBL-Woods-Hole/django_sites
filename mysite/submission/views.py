from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.utils.html import escape
import os 

def my_view(request):
    context = {'foo': 'bar'}
    return render(request, 'my_template.html', context)
from .models_l_env454 import Run

from .forms import RunForm, FileUploadForm, CsvRunInfoUploadForm, MetadataOutCsvForm, AddProjectForm
from .utils import Run, Utils

from .metadata_tools import CsvMetadata
# , Validation

def index(request):
    latest_run_list = Run.cache_all_method.order_by('-run')[:10]
    context = {'latest_run_list': latest_run_list}
    current_url = request.META["HTTP_REFERER"]

    return render(request, current_url, context)

def help(request):
    return render(request, 'submission/help.html', {'header': 'Help and tips'})

def upload_metadata(request):

    # error_message = ""
    """TODO:
    https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    Form.errors
    """
    utils = Utils()
    csv_handler = CsvMetadata()
    
    if request.method == 'POST' and request.FILES:
        utils.clear_session(request)
        
        metadata_run_info_form, metadata_new_project_form = csv_handler.csv_file_upload(request)

        return render(request, 'submission/upload_metadata.html', {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'errors': csv_handler.errors, 'metadata_new_project_form': metadata_new_project_form })
        
    elif 'submit_new_project' in request.POST:

        metadata_run_info_form, metadata_new_project_form = csv_handler.submit_new_project(request)
    
        return render(request, 'submission/upload_metadata.html', {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'errors': csv_handler.errors, 'metadata_new_project_form': metadata_new_project_form, 'new_project_name': csv_handler.new_project, 'new_project_created': csv_handler.new_project_created })
    

    elif 'submit_run_info' in request.POST:

        request, metadata_run_info_form, formset = csv_handler.submit_run_info(request)
        
        errors_size = len(metadata_run_info_form.errors)
        
        if errors_size > 0:
            context = {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'errors': csv_handler.errors, 'errors_size': errors_size }
        else:
            context = {'metadata_run_info_form': metadata_run_info_form, 'metadata_out_csv_form': formset, 'out_metadata_table': csv_handler.out_metadata_table}

        return render(request, 'submission/upload_metadata.html', context)

    elif 'create_submission_metadata_file' in request.POST:
        
        request, metadata_run_info_form, formset = csv_handler.create_submission_metadata_file(request)
        
        context = {'metadata_run_info_form': metadata_run_info_form, 'metadata_out_csv_form': formset, 'out_metadata_table': request.session['out_metadata_table'], 'errors': formset.errors, 'errors_size': formset.total_error_count(), 'files_created': csv_handler.files_created}
        
    else:
        file_upload_form = FileUploadForm()
        
        context = {'file_upload_form': file_upload_form, 'header': 'Upload metadata', 'formset': {}}

    return render(request, 'submission/upload_metadata.html', context)

# def my_view(request):
#     context = {'foo': 'bar'}
#     return render_to_response('my_template.html', context, context_instance=RequestContext(request))
#
# def my_view(request):
#     context = {'foo': 'bar'}
#     return render(request, 'my_template.html', context)

def data_upload(request):
    run_utils = Run()

    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Data upload to db', 'is_cluster': 'not', 'pipeline_command': 'env454upload',  'error_message': error_message})

def run_info_upload(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Run info upload to db', 'is_cluster': 'not', 'pipeline_command': 'env454run_info_upload',  'error_message': error_message })

def chimera_checking(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Chimera checking (for v4v5 region only)', 'is_cluster': '', 'pipeline_command': 'illumina_chimera_only', 'what_to_check': 'statistics ', 'check_command': 'chimera/; chimera_stats.py', 'error_message': error_message})

def demultiplex(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Demultiplex Illumina files by index/run_key/lane', 'is_cluster': 'not', 'pipeline_command': 'illumina_files_demultiplex_only',  'error_message': error_message })

def overlap(request):
    run_utils = Run()
    run_data = {}
    check_command = ''
    try:
        form, run_data, error_message = run_utils.get_run(request)
        check_command = 'reads_overlap/; take_%s_stats.py' % run_data['find_machine']
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap, filter and unique reads in already demultiplexed files', 'is_cluster': '', 'pipeline_command': 'illumina_files', 'what_to_check': 'the overlap percentage ', 'check_command': check_command, 'error_message': error_message })

def overlap_only(request):
    run_utils = Run()
    run_data = {}
    check_command = ''
    try:
        form, run_data, error_message = run_utils.get_run(request)
        check_command = 'reads_overlap/; take_%s_stats.py' % run_data['find_machine']
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap reads in already demultiplexed files', 'is_cluster': '', 'command': '; run_partial_overlap_clust.sh; date', 'what_to_check': 'the overlap percentage ', 'check_command': check_command, 'error_message': error_message })

def filter_mismatch(request):
    run_utils = Run()
    run_data = {}
    header = '''Filtering partial (Ev4, v4v5 and ITS1) merged\n
    Maximum number of mismatches allowed in the overlapped region is 3'''
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': header, 'is_cluster': '', 'command': 'reads_overlap/; run_mismatch_filter.sh; date',  'error_message': error_message })

def gast(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
        # print "!!!form.cleaned_data"
        # print form.cleaned_data
        # print "555 find_rundate = "
        # print run_data['find_rundate']
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gast', 'is_cluster': 'not', 'command': 'reads_overlap/; run_gast_ill_nonchim_sge.sh; date', 'what_to_check': 'the percent of "Unknown" taxa ', 'check_command': 'gast/; percent10_gast_unknowns.sh', 'error_message': error_message})

def gzip_all(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gzip all files', 'is_cluster': 'not', 'command': '; time gzip -r *',  'error_message': error_message})

def clear_db(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/clear_db.html', {'form': form, 'run_data': run_data, 'header': 'Remove old data from db',  'error_message': error_message})

def uniqueing(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Uniqueing fasta files', 'is_cluster': '', 'command': 'reads_overlap/; run_unique_fa.sh; date',  'error_message': error_message })

def check_fa_counts(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Check counts in fasta files', 'is_cluster': 'not', 'command': 'reads_overlap/; grep '>' *REMOVED.unique | wc -l; date',  'error_message': error_message})

def check_db_counts(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/check_db_counts.html', {'form': form, 'run_data': run_data, 'header': 'Check counts in db', 'error_message': error_message})

def gunzip_all(request):
    run_utils = Run()
    run_data = {}
    try:
        form, run_data, error_message = run_utils.get_run(request)
    except:
        form, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gunzip all files', 'is_cluster': 'not', 'command': '; time gunzip -r *.gz',  'error_message': error_message})