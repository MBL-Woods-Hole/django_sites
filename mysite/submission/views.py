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
    if request.method == 'POST' and request.FILES:
        # print "POST, request"
        # print HttpResponse(escape(repr(request)))
        
        # for key, value in request.POST.items():
        #   print(key, value)
        # 
        # print "===="
        # print "request.META = %s" % (request.META)
#         request.META = {'RUN_MAIN': 'true'
# , 'HTTP_REFERER': 'http://localhost:8000/submission/upload_metadata/'
# , 'rvm_version': '1.25.25 (stable)'
# , 'SERVER_PROTOCOL': 'HTTP/1.1'
# , 'SERVER_SOFTWARE': 'WSGIServer/0.1 Python/2.7.12'
# , 'rvm_path': '/Users/ashipunova/.rvm'
# , 'TERM_PROGRAM_VERSION': '377'
# , 'RUBY_VERSION': 'ruby-1.9.3-p448'
# , 'REQUEST_METHOD': 'POST'
# , 'LOGNAME': 'ashipunova'
# , 'USER': 'ashipunova'
# , 'PATH': '/usr/local/bin:/opt/local/bin:/opt/local/sbin:/Users/ashipunova/.rvm/gems/ruby-1.9.3-p448@rails3tutorial2ndEd/bin:/Users/ashipunova/.rvm/gems/ruby-1.9.3-p448@global/bin:/Users/ashipunova/.rvm/rubies/ruby-1.9.3-p448/bin:/Users/ashipunova/.rvm/bin:/Users/ashipunova/.rvm/bin:/usr/local/bin:/usr/local/mysql/bin:/Library/Frameworks/Python.framework/Versions/2.7/bin:/opt/local/bin:/opt/local/sbin:/Developer/usr/bin:/Users/ashipunova/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/X11/bin:/Applications/OpenOffice.app/Contents/MacOS'
# , 'QUERY_STRING': ''
# , 'HOME': '/Users/ashipunova'
# , 'DISPLAY': '/private/tmp/com.apple.launchd.IgL8qcIfe7/org.macosforge.xquartz:0'
# , 'TERM_PROGRAM': 'Apple_Terminal'
# , 'LANG': 'C'
# , 'HISTCONTROL': 'ignoreboth'
# , 'TERM': 'xterm-256color'
# , 'SHELL': '/bin/bash'
# , 'TZ': 'America/New_York'
# , 'HTTP_COOKIE': '_ga=GA1.1.793822726.1445886513; csrftoken=JUxrGn2ToAH84e4fJeAQzyQVexaPQmXtG9uKylRIAzIeYyNqKJoSWsmrZBSBbXdA; PHPSESSID=h1pgtp94mvq25mibu2a25dt754; djdt=show'
# , 'SERVER_NAME': '1.0.0.127.in-addr.arpa'
# , 'REMOTE_ADDR': '127.0.0.1'
# , 'SHLVL': '1'
# , 'SECURITYSESSIONID': '186a7'
# , '_system_name': 'OSX'
# , 'XPC_FLAGS': '0x0'
# , 'HISTSIZE': '100000'
# , 'wsgi.url_scheme': 'http'
# , 'SERVER_PORT': '8000'
# , '_': '/usr/local/bin/python'
# , 'MANPATH': '/opt/local/share/man:'
# , 'CONTENT_LENGTH': '1452'
# , 'SVN_EDITOR': 'mate'
# , 'GEM_PATH': '/Users/ashipunova/.rvm/gems/ruby-1.9.3-p448@rails3tutorial2ndEd:/Users/ashipunova/.rvm/gems/ruby-1.9.3-p448@global'
# , 'rvm_bin_path': '/Users/ashipunova/.rvm/bin'
# , 'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
# , 'TERM_SESSION_ID': 'A8E25A18-81BE-443C-B964-A4DB261E75B9'
# , 'XPC_SERVICE_NAME': '0'
# , 'CONTENT_TYPE': 'multipart/form-data; boundary=---------------------------220127776015557552142047856'
# , 'rvm_prefix': '/Users/ashipunova'
# , 'PYTHONPATH': '/usr/local/bin:'
# , 'SSH_AUTH_SOCK': '/private/tmp/com.apple.launchd.OITrIGZplo/Listeners'
# , 'IRBRC': '/Users/ashipunova/.rvm/rubies/ruby-1.9.3-p448/.irbrc'
# , 'LC_CTYPE': 'en_US.UTF-8'
# , 'MY_RUBY_HOME': '/Users/ashipunova/.rvm/rubies/ruby-1.9.3-p448'
# , 'wsgi.input': <socket._fileobject object at 0x104a636d0>
# , 'Apple_PubSub_Socket_Render': '/private/tmp/com.apple.launchd.2erxpCm2fa/Render'
# , 'HTTP_HOST': 'localhost:8000'
# , 'SCRIPT_NAME': u''
# , 'wsgi.multithread': True
# , 'HTTP_CONNECTION': 'keep-alive'
# , 'HTTP_UPGRADE_INSECURE_REQUESTS': '1'
# , '_system_type': 'Darwin'
# , 'TMPDIR': '/var/folders/hk/ttq4v2596xq66wxc6f5j987m0000gn/T/'
# , 'HISTIGNORE': '&:bg:fg:ll:h: cd'
# , '_system_arch': 'x86_64'
# , 'wsgi.version': (1
# , 0)
# , 'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0'
# , 'GATEWAY_INTERFACE': 'CGI/1.1'
# , 'wsgi.run_once': False
# , u'CSRF_COOKIE': 'JUxrGn2ToAH84e4fJeAQzyQVexaPQmXtG9uKylRIAzIeYyNqKJoSWsmrZBSBbXdA'
# , 'OLDPWD': '/Users/ashipunova'
# , 'wsgi.multiprocess': False
# , 'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5'
# , 'wsgi.errors': <open file '<stderr>'
# , mode 'w' at 0x102c141e0>
# , 'HTTP_ACCEPT_ENCODING': 'gzip
# , deflate'
# , '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'
# , 'PWD': '/Users/ashipunova/BPC/python_web/django_sites/mysite'
# , 'DJANGO_SETTINGS_MODULE': 'mysite.settings'
# , '_system_version': '10.12'
# , 'wsgi.file_wrapper': <class wsgiref.util.FileWrapper at 0x103f6bbb0>
# , 'REMOTE_HOST': ''
# , 'GEM_HOME': '/Users/ashipunova/.rvm/gems/ruby-1.9.3-p448@rails3tutorial2ndEd'
# , 'PATH_INFO': u'/submission/upload_metadata/'}
#       
        form = CsvRunInfoUploadForm(request.POST)
        print "form: %s \n=======" % form
        
        
        csv_file = request.FILES['csv_file']
        csv_handler = CsvMetadata()
        
        csv_handler.import_from_file(csv_file)
        # csv_validation = Validation()
        # csv_validation.required_cell_values_validation()

        csv_handler.get_selected_variables()
        csv_handler.get_initial_run_info_data_dict()
        metadata_run_info_form = CsvRunInfoUploadForm(initial=csv_handler.run_info_from_csv)
        # TODO: move to one method in metadata_tools, call from here as create info and create csv
        csv_handler.get_lanes_domains()
        csv_handler.create_path_to_csv()
        csv_handler.create_ini_names()
        csv_handler.write_ini()
        csv_handler.get_vamps_submission_info()
        csv_handler.make_all_out_metadata()
        csv_handler.make_metadata_table()
        
        # TODO: create form
        # metadata_out_csv_form = 

        utils.is_local(request)
        # HOSTNAME = request.get_host()
        # if HOSTNAME.startswith("localhost"):
        #     print "local"

        return render(request, 'submission/upload_metadata.html', {'metadata_run_info_form': metadata_run_info_form, 'header': 'Upload metadata', 'csv_by_header_uniqued': csv_handler.csv_by_header_uniqued, 'metadata_out_csv_form': csv_handler.out_metadata_table, 'errors': csv_handler.errors })
        
    elif 'submit_run_info' in request.POST:
        print "EEE: request.POST = %s" % request.POST
        return render(request, 'submission/upload_metadata__run_info_form.html', {'metadata_run_info_form': metadata_run_info_form})

    # elif 'create_submission_metadata_file' in request.POST:
    #     print "EEE: request.POST = %s" % request.POST
    #     return render(request, 'submission/upload_metadata__run_info_form.html', {'metadata_run_info_form': metadata_run_info_form})

        
    else:
        # print "EEE"

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

def upload_metadata__run_info_form(request):
    print "EEE1: request.POST = %s" % request.POST
    
    metadata_run_info_form = CsvRunInfoUploadForm(request.POST)
    if metadata_run_info_form.is_valid():
        print "form CsvRunInfoUploadForm: form.cleaned_data: %s \n=======" % metadata_run_info_form.cleaned_data
    
    return render(request, 'submission/upload_metadata__run_info_form.html', {'metadata_run_info_form': metadata_run_info_form})
    
    
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