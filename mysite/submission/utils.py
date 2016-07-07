from .forms import RunForm
import models 
from models_l_env454 import RunInfoIll

def get_overlap(machine_name):
    overlap_choices = dict(models.Overlap.COMPLETE_OVERLAP_CHOICES)
    return overlap_choices[machine_name]
    
def get_full_macine_name(machine_name):
    machine_choices = dict(models.Machine.MACHINE_CHOICES) 
    return machine_choices[machine_name]

def get_domain_name(domain_name):
    domain_choices = dict(models.Domain.SUITE_DOMAIN_CHOICES) 
    print "DDD domain_choices"
    print domain_choices
    return domain_choices[domain_name]
    
def get_primer_suites(run, lane, suite_domain):
    all_suites = RunInfoIll.objects.filter(run__run = run, lane = lane)
    primer_suites = set([entry.primer_suite for entry in all_suites if entry.primer_suite.primer_suite.startswith(suite_domain)])
    try:
      return (True, next(iter(primer_suites)).primer_suite)
    except StopIteration:
      error_message = "There is no such combination in our database: run = %s, lane = %s, and domain = %s" % (run, lane, suite_domain)
      return (False, error_message)
    except:
      raise
    '''
    
    for ps in set(ee):
        if ps.primer_suite.startswith('Bacterial'):
            print ps
    
    from submission.models_l_env454 import RunInfoIll
    
    a = RunInfoIll.objects.filter(run__run='20160504', lane='1')
    type(a)
    for entry in a:
        print entry.primer_suite
    for entry in a:
        print "%s, %s" % (entry.primer_suite, entry.dna_region)
    
    ee = [entry.primer_suite for entry in a]
    set(ee)
    {<PrimerSuite: Bacterial V4-V5 Suite>, <PrimerSuite: Archaeal V4-V5 Suite>}

    
    $query = "
  SELECT DISTINCT primer_suite, dna_region
       FROM " . $db_name . ".run_info_ill
       JOIN " . $db_name . ".run USING(run_id)
       JOIN " . $db_name . ".dna_region USING(dna_region_id)
       JOIN " . $db_name . ".primer_suite USING(primer_suite_id)
       WHERE
       run = \"" . $rundate . "\"
       AND lane = " . $lane . "      
        ";'''

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
            run_data['full_machine_name'] = get_full_macine_name(form.cleaned_data['find_machine'])
            run_data['perfect_overlap']   = get_overlap(form.cleaned_data['find_machine'])
            run_data['suite_domain']      = get_domain_name(form.cleaned_data['find_domain'])
            primer_suite = get_primer_suites(run_data['find_rundate'], run_data['find_lane'], run_data['suite_domain'])
            if (run_data['primer_suite'][0]):
              run_data['primer_suite']
            print "run_data: "
            print run_data
            
            return (form, run_data)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RunForm()
    return form
