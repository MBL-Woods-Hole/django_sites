from .forms import RunForm, FileUploadForm, CsvRunInfoUploadForm
import models
from models_l_env454 import RunInfoIll
# from .csv_tools import CsvMetadata

import time
import os

class Utils():

    def benchmark_w_return_1(self):
        print  "\n"
        print "-" * 10
        return time.time()

    def benchmark_w_return_2(self, t0):
        t1 = time.time()
        total = float(t1-t0) / 60
        # print 'time: %.2f m' % total
        print 'time: %f s' % total

    def is_local(self, request):
        hostname = request.get_host()
        if hostname.startswith("localhost"):
            return True
        else:
            return False

    def get_overlap(self, machine_name):
        overlap_choices = dict(models.Overlap.COMPLETE_OVERLAP_CHOICES)
        return overlap_choices[machine_name]

    def get_full_macine_name(self, machine_name):
        machine_choices = dict(models.Machine.MACHINE_CHOICES)
        return machine_choices[machine_name]

    def get_domain_name(self, domain_name):
        domain_choices = dict(models.Domain.SUITE_DOMAIN_CHOICES)
        return domain_choices[domain_name]
            

class Dirs:
    """
        input_dir - directory with fastq files
    """
    def __init__(self):
        self.utils = Utils()
        self.output_dir_name = None
        self.get_path()
        
    def check_and_make_dir(self, dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            if os.path.isdir(dir_name):
                print "\nDirectory %s already exists."  % (dir_name)
            else:
                raise    
        return dir_name
    
    def check_dir(self, dir_name):
        if os.path.isdir(dir_name):
            return dir_name
        else:            
            return self.check_and_make_dir(dir_name) 
            
    def get_path(self):
        if self.utils.is_local():
            root_dir  = C.output_root_mbl_local
    
        self.output_dir = os.path.join(root_dir, platform, id_number)    
        if (lane_name != ''):
            self.output_dir = os.path.join(root_dir, platform, id_number, lane_name)
            
class Run():
    def __init__(self):
        self.utils = Utils()
    
    def get_primer_suites(self, run, lane, suite_domain):
        all_suites = RunInfoIll.objects.filter(run__run = run, lane = lane)
        primer_suites = set([entry.primer_suite for entry in all_suites if entry.primer_suite.primer_suite.startswith(suite_domain)])
        try:
          return (True, next(iter(primer_suites)).primer_suite)
        except StopIteration:
          error_message = "There is no such combination in our database: run = %s, lane = %s, and domain = %s" % (run, lane, suite_domain)
          return (False, error_message)
        except:
          raise

    def get_run(self, request):
        print "Running get_run from utils"
        error_message = ""
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
                run_data['full_machine_name'] = self.utils.get_full_macine_name(form.cleaned_data['find_machine'])
                run_data['perfect_overlap']   = self.utils.get_overlap(form.cleaned_data['find_machine'])
                suite_domain                  = self.utils.get_domain_name(form.cleaned_data['find_domain'])
                primer_suite = self.get_primer_suites(run_data['find_rundate'], run_data['find_lane'], suite_domain)
                print "primer_suite[1]"

                print primer_suite[1]

                if (primer_suite[0]):
                    run_data['primer_suite'] = primer_suite[1]
                else:
                    error_message = primer_suite[1]
                print "run_data: "
                print run_data

                return (form, run_data, error_message)
        # if a GET (or any other method) we'll create a blank form
        else:
            form = RunForm()
        return (form, error_message)
