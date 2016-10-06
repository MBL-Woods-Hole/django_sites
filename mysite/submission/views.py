from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.utils.html import escape

def my_view(request):
    context = {'foo': 'bar'}
    return render(request, 'my_template.html', context)
from .models_l_env454 import Run

from .forms import RunForm, CsvRunInfoUploadForm, FileUploadForm
from .utils import Run, Utils

from .metadata_tools import CsvMetadata, Validation

def index(request):
    latest_run_list = Run.objects.order_by('-run')[:10]
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
        form = CsvRunInfoUploadForm(request.POST)
        # print "form: %s \n=======" % form
        
        
        csv_file = request.FILES['csv_file']
        # csv_handler = CsvMetadata()
        
        csv_handler.import_from_file(csv_file)
        # csv_validation = Validation()
        # csv_validation.required_cell_values_validation()

        csv_handler.get_selected_variables(request.POST)
        csv_handler.get_initial_run_info_data_dict()
        metadata_run_info_form = CsvRunInfoUploadForm(initial=csv_handler.run_info_from_csv)
        print "FFF csv_handler.run_info_from_csv = %s" % csv_handler.run_info_from_csv
        
        # # TODO: move to one method in metadata_tools, call from here as create info and create csv
        # csv_handler.get_lanes_domains()
        # csv_handler.create_path_to_csv()
        # csv_handler.create_ini_names()
        # csv_handler.write_ini()
        csv_handler.get_vamps_submission_info()
        csv_handler.make_new_out_metadata()
        
        request.session['out_metadata'] = csv_handler.out_metadata
        print "request.session.keys() = %s" % request.session.keys()
        print "request.session.values() = %s" % request.session.values()
        # csv_handler.make_metadata_table()
        
        # TODO: create form
        # metadata_out_csv_form = 
        
        # TODO: use to get db_names
        print "utils.is_local(request) = %s" % utils.is_local(request)
        # utils.is_local(request) = True
        
        # utils.is_local(request)
        # HOSTNAME = request.get_host()
        # if HOSTNAME.startswith("localhost"):
        #     print "local"

        return render(request, 'submission/upload_metadata.html', {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'errors': csv_handler.errors })
        
    elif 'submit_run_info' in request.POST:
        print "EEE: request.POST = %s" % request.POST
        # TODO: move to one method in metadata_tools, call from here as create info and create csv
        csv_handler.get_selected_variables(request.POST)
        csv_handler.get_lanes_domains()
        csv_handler.create_path_to_csv()
        csv_handler.create_ini_names()
        csv_handler.write_ini()
        # csv_handler.get_vamps_submission_info()
        # TODO: call to ajust?
        csv_handler.edit_out_metadata(request)
        print "request.session.keys()1 = %s" % request.session.keys()
        print "request.session 1= %s" % request.session
        print "request.session.values()1 = %s" % request.session.values()
        
        csv_handler.make_metadata_table()
        
        metadata_run_info_form = CsvRunInfoUploadForm(request.POST)        
        return render(request, 'submission/upload_metadata.html', {'metadata_run_info_form': metadata_run_info_form, 'metadata_out_csv_form': csv_handler.out_metadata_table})

    # elif 'create_submission_metadata_file' in request.POST:
    #     print "EEE: request.POST = %s" % request.POST
    #     return render(request, 'submission/upload_metadata.html', {'metadata_run_info_form': metadata_run_info_form})

    else:
        file_upload_form = FileUploadForm()
        context = {'file_upload_form':file_upload_form, 'header': 'Upload metadata'}

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