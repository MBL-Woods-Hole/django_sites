# from .models_l_env454 import Run
from .forms import RunForm

def get_run(request):
    print "Running get_run from utils"
    run_data = {}
    if request.method == 'POST':
        form = RunForm(request.POST)
        print "request.POST = "
        print request.POST
        if form.is_valid():
            run_data['find_rundate'] = form.cleaned_data['find_rundate'].run
            run_data['find_machine'] = form.cleaned_data['find_machine']
            run_data['find_domain']  = form.cleaned_data['find_domain']
            run_data['find_lane']    = form.cleaned_data['find_lane']

            return (form, run_data)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RunForm()
    return form

def where_to_run(is_cluster):
    "This command line(s) can be run on any %s cluster:" % is_cluster
    
#
#
#   $pipeline_command = "env454upload";
#
#   include_once("steps_command_line.php");
#   server_message("any");
#
#
#   include_once("steps_command_line_print.php");
#
# This command line(s) can be run on any not cluster:
# Please check if the path to raw data exists: /xraid2-2/sequencing/Illumina/20160624
# cd /xraid2-2/g454/run_new_pipeline/illumina/hiseq_info/20160624; time python /bioware/linux/seqinfo/bin/python_pipeline/py_mbl_sequencing_pipeline/pipeline-ui.py -csv /xraid2-2/g454/run_new_pipeline/illumina/hiseq_info/20160624/metadata_20160624_1_B.csv -s env454upload -l debug -p illumina -r 20160624 -ft fastq -i /xraid2-2/sequencing/Illumina/20160624 -cp True -lane_name lane_1_B -do_perfect True
