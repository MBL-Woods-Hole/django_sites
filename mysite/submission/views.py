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
import logging


# def my_view(request):
#     context = {'foo': 'bar'}
#     return render(request, 'my_template.html', context)
from .models_l_env454 import Run as models_run

# from .forms import RunForm, FileUploadForm, CsvRunInfoUploadForm, MetadataOutCsvForm, AddProjectForm
from .forms import FileUploadForm, AddProjectForm
from .utils import Run, Utils

from .metadata_tools import CsvMetadata
# , Validation

def index(request):
    latest_run_list = models_run.cache_all_method.order_by('-run')[:10]
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
    csv_handler = CsvMetadata(request)

    if request.method == 'POST' and request.FILES:
        context = upload_file_n_make_new_metadata(request)

    elif 'submit_run_info' in request.POST:
        context = submit_run_info_n_edit_metadata_n_make_table(request)

    elif 'create_submission_metadata_file' in request.POST:
        context = edit_metadata_table_n_add_metadata_table_to_metadata_n_update_metadata(request)
    else:
        context = initial_form()

    return render(request, 'submission/upload_metadata.html', context)

def upload_file_n_make_new_metadata(request):
    utils = Utils()
    csv_handler = CsvMetadata(request)
    
    logging.debug("HHH")
    logging.debug("111 request.method == 'POST' and request.FILES:")
    utils.clear_session(request)

    metadata_run_info_form, has_file_errors = csv_handler.csv_file_upload(request)

    if has_file_errors == 'no_file':
        errors_size = len(csv_handler.errors)
        context = {'header': 'Upload metadata', 'errors': csv_handler.errors, 'errors_size': errors_size}

        render(request, 'submission/upload_metadata.html', context)

    if has_file_errors == 'has_empty_cells':
        errors_size = len(csv_handler.empty_cells)

        context = {'header': 'Upload metadata', 'errors': csv_handler.errors, 'errors_size': errors_size}

        render(request, 'submission/upload_metadata.html', context)

    errors_size = len(csv_handler.errors)

    return {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'errors': csv_handler.errors, 'errors_size': errors_size }
    
def submit_run_info_n_edit_metadata_n_make_table(request):
    csv_handler = CsvMetadata(request)
    
    logging.debug("HHH")
    logging.debug("333 submit_run_info in request.POST")

    request, metadata_run_info_form, formset = csv_handler.submit_run_info(request)

    errors_size = len(metadata_run_info_form.errors)

    if errors_size > 0:
        context = {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'errors': csv_handler.errors, 'errors_size': errors_size }
    else:
        context = {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'metadata_out_csv_form': formset, 'out_metadata_table': csv_handler.out_metadata_table}
    return context
            
def edit_metadata_table_n_add_metadata_table_to_metadata_n_update_metadata(request):
    csv_handler = CsvMetadata(request)
    logging.debug("HHH")
    logging.debug("444 create_submission_metadata_file in request.POST")

    request, metadata_run_info_form, formset = csv_handler.create_submission_metadata_file(request)

    errors_size = formset.total_error_count()

    return {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'metadata_out_csv_form': formset, 'out_metadata_table': request.session['out_metadata_table'], 'errors': formset.errors, 'errors_size': errors_size, 'files_created': csv_handler.files_created}

def initial_form():
    logging.debug("HHH")
    logging.debug("555 file_upload_form")

    file_upload_form = FileUploadForm()

    return {'file_upload_form': file_upload_form, 'header': 'Upload metadata', 'formset': {}}
        
def add_project(request):
    csv_handler = CsvMetadata(request)

    if request.method == 'POST':
        # elif 'submit_new_project' in request.POST:
        logging.debug("HHH")
        logging.debug("222 submit_new_project in request.POST")

        metadata_new_project_form = csv_handler.submit_new_project(request)

        context = {'header': 'Add New Project', 'errors': csv_handler.errors, 'metadata_new_project_form': metadata_new_project_form, 'new_project_name': csv_handler.new_project, 'new_project_created': csv_handler.new_project_created}    
    else:
        metadata_new_project_form = AddProjectForm()
        context = {'header': 'Add New Project', 'errors': csv_handler.errors, 'metadata_new_project_form': metadata_new_project_form}
    return render(request, 'submission/add_project.html', context)

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
    form, run_data, error_message = run_utils.get_run(request)

    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Data upload to db (Please run twice, both for env454 and vamps2)', 'is_cluster': 'not', 'pipeline_command': 'file_to_db_upload', 'error_message': error_message})

def run_info_upload(request):
    run_utils = Run()
    run_data = {}

    form, run_data, error_message = run_utils.get_run(request)

    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Run info upload to db', 'is_cluster': 'not', 'pipeline_command': 'run_info_upload',  'error_message': error_message })

def chimera_checking(request):
    run_utils = Run()
    run_data = {}

    form, run_data, error_message = run_utils.get_run(request)

    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Chimera checking (not needed for v6 region)', 'is_cluster': '', 'pipeline_command': 'illumina_chimera_only', 'what_to_check': 'statistics ', 'check_command': 'chimera/; chimera_stats.py', 'error_message': error_message})

def demultiplex(request):
    run_utils = Run()
    run_data = {}
    
    form, run_data, error_message = run_utils.get_run(request)
    
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Demultiplex Illumina files by index/run_key/lane', 'is_cluster': 'not', 'pipeline_command': 'illumina_files_demultiplex_only',  'error_message': error_message })

def overlap(request):
    run_utils = Run()
    run_data = {}
    check_command = ''

    form, run_data, error_message = run_utils.get_run(request)

    try:
        check_command = 'reads_overlap/; take_%s_stats.py' % run_data['find_machine']
    except:
        pass
    
    return render(request, 'submission/page_w_command_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap, filter and unique reads in already demultiplexed files', 'is_cluster': '', 'pipeline_command': 'illumina_files', 'what_to_check': 'the overlap percentage ', 'check_command': check_command, 'error_message': error_message })

def overlap_only(request):
    run_utils = Run()
    run_data = {}
    check_command = ''
    form, run_data, error_message = run_utils.get_run(request)
    try:
        check_command = 'reads_overlap/; take_%s_stats.py' % run_data['find_machine']
    except:
        pass
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Overlap reads in already demultiplexed files', 'is_cluster': '', 'command': '; run_partial_overlap_clust.sh; date', 'what_to_check': 'the overlap percentage ', 'check_command': check_command, 'error_message': error_message })

def filter_mismatch(request):
    run_utils = Run()
    run_data = {}
    header = '''Filtering partial (Ev4, v4v5 and ITS1) merged\n
    Maximum number of mismatches allowed in the overlapped region is 3'''
    
    form, run_data, error_message = run_utils.get_run(request)
    
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': header, 'is_cluster': '', 'command': 'reads_overlap/; run_mismatch_filter.sh; date',  'error_message': error_message })

def gast(request):
    # utils = Utils()
    # utils.clear_session(request)
    #TODO: remove!
    # try:
    #     del request.session['run_info']
    # except:
    #     pass
    run_utils = Run()
    run_data = {}

    # from django.db import connections
    # cursor = connections['vamps'].cursor()
    # logging.debug("RRR")
    # logging.debug("connections['vamps']")
    # aa = connections['vamps'].get_connection_params()
    # logging.debug("connections['vamps'].get_connection_params()['db']")
    # logging.debug(aa['db'])
    # logging.debug("connections['vamps'].queries")
    # logging.debug(connections['vamps'].queries)
    # db_name = "vamps"
    # submit_code = "lmaignien_177212"
    # logging.debug("db_name = %s, submit_code = %s" % (db_name, submit_code))
    # logging.debug("db_name = %s, submit_code = %s" % (db_name, submit_code))
    # query_subm = """SELECT subm.*, auth.username, auth.encrypted_password, auth.first_name, auth.last_name, auth.active, auth.security_level, auth.email, auth.institution, auth.current_sign_in_at, auth.last_sign_in_at
    #                 FROM %s.vamps_submissions AS subm
    #                 JOIN vamps2.user AS auth
    #                   USING(user_id)
    #                 WHERE submit_code = \"%s\"""" % (db_name, submit_code)
    #
    #
    
    form, run_data, error_message = run_utils.get_run(request)    
    
    # print "FFF form"
    # print form

    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gast', 'is_cluster': '', 'command': 'reads_overlap/; run_gast_ill_nonchim_sge.sh; date', 'what_to_check': 'the percent of "Unknown" taxa ', 'check_command': 'gast/; percent10_gast_unknowns.sh', 'error_message': error_message})

def gzip_all(request):
    run_utils = Run()
    run_data = {}

    form, run_data, error_message = run_utils.get_run(request)
    try:
        info_dir = os.path.join(settings.ILLUMINA_RES_DIR, run_data['full_machine_name'] + "_info/", run_data['find_rundate'])
        gzip_not_gzipped = 'find . -type f ! -name "*gz*" -exec gzip {} \;'
        gzip_command = '; ' + gzip_not_gzipped + ' ; cd %s; ' % (info_dir) + gzip_not_gzipped
        return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gzip all files', 'is_cluster': 'not', 'command': gzip_command, 'error_message': error_message})

    except:
        info_dir = settings.ILLUMINA_RES_DIR
        error_message = "Please check run info."
    
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gzip all files', 'error_message': error_message})

def clear_db(request):
    run_utils = Run()
    run_data = {}

    form, run_data, error_message = run_utils.get_run(request)
    table_names = {"vamps2": {"pdr": "sequence_pdr_info", "uniq": "sequence_uniq_info", "seq": "sequence", "join_pr": "", "run_info_join": "dataset"}, "env454": {"pdr": "sequence_pdr_info_ill", "uniq": "sequence_uniq_info_ill", "seq": "sequence_ill", "join_pr": " JOIN project using(project_id) ", "run_info_join": "run_info_ill"}}

    return render(request, 'submission/clear_db.html', {'form': form, 'run_data': run_data, 'header': 'Remove old data from db', 'table_names': table_names[run_data['find_db_name']], 'error_message': error_message})

def uniqueing(request):
    run_utils = Run()
    run_data = {}
    form, run_data, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Uniqueing fasta files', 'is_cluster': '', 'command': 'reads_overlap/; run_unique_fa.sh; date',  'error_message': error_message })

def check_fa_counts(request):
    from .model_choices import File_name
    file_names = File_name()
    file_name_choices = dict(file_names.FILE_NAME_CHOICES)
    
    run_utils = Run()
    run_data = {}
    command_line = ""
    form, run_data, error_message = run_utils.get_run(request)
    try:
      command_line = "reads_overlap/; grep \'>\' *%s | wc -l; date" % (file_name_choices[run_data['find_machine']])
    except KeyError:
      # command_line = "reads_overlap/; grep \'>\' *.fa | wc -l; date" % (file_name_choices[run_data['find_machine']])
      logging.debug("FFF run_data")
      logging.debug(run_data)
      # pass
    except:
      raise
      
    
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Check counts in fasta files', 'is_cluster': 'not', 'command': command_line,  'error_message': error_message})

def check_db_counts(request):
    run_utils = Run()
    run_data = {}
    form, run_data, error_message = run_utils.get_run(request)
    return render(request, 'submission/check_db_counts.html', {'form': form, 'run_data': run_data, 'header': 'Check counts in db', 'error_message': error_message})

def gunzip_all(request):
    run_utils = Run()
    run_data = {}
    gunzip_command = "; time find . -name '*.gz' -exec sh -c 'gunzip {}' ';'"
    form, run_data, error_message = run_utils.get_run(request)
    return render(request, 'submission/page_wo_c_l.html', {'form': form, 'run_data': run_data, 'header': 'Gunzip all files', 'is_cluster': 'not', 'command': gunzip_command,  'error_message': error_message})

