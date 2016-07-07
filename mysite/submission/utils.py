from .forms import RunForm
import models 
# import Machine, Overlap

def get_overlap(machine_name):
    overlap_choices = dict(models.Overlap.COMPLETE_OVERLAP_CHOICES)
    return overlap_choices[machine_name]
    
def get_full_macine_name(machine_name):
    machine_choices = dict(models.Machine.MACHINE_CHOICES) 
    return machine_choices[machine_name]

def get_domain_name(domain_name):
    domain_choices = dict(models.Domain.SUITE_DOMAIN_CHOICES) 
    print "DDD domain_choices"
    return domain_choices[domain_name]

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
            run_data['suite_domain']      = get_domain_name((form.cleaned_data['find_domain']))
            
            print "run_data: "
            print run_data
            
            return (form, run_data)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RunForm()
    return form
