from .forms import RunForm, FileUploadForm, CsvRunInfoUploadForm
import models
# from models_l_env454 import RunInfoIll
import models_l_env454


import time
import os
import logging

class Utils():

    def benchmark_w_return_1(self):
        logging.info("\n")
        logging.info("-" * 10)
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

    def clear_session(self, request):
        for key in request.session.keys():
            del request.session[key]
            
    # TODO: combine with metadata_utils, DRY!
    def get_lanes_domains(self, out_metadata):
        domain_choices = dict(models.Domain.LETTER_BY_DOMAIN_CHOICES)
        lanes_domains = []
            
        for idx, val in out_metadata.items():
            domain_letter = domain_choices[val['domain']]
            lanes_domains.append("%s_%s" % (val['lane'], domain_letter))
        # logging.debug("self.lanes_domains = %s" % self.lanes_domains)
        return lanes_domains



class Dirs:
    """
        input_dir - directory with fastq files
    """
    def __init__(self):
        self.utils = Utils()
        self.output_dir_name = None
        # self.get_path()

    def check_and_make_dir(self, dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            if os.path.isdir(dir_name):
                logging.info("\nDirectory %s already exists."  % (dir_name))
            else:
                raise    
        return dir_name

    def check_dir(self, dir_name):
        if os.path.isdir(dir_name):
            return dir_name
        else:            
            return self.check_and_make_dir(dir_name) 

    def get_path(self):
        # logging.info("request.META['HTTP_HOST'] = %s" % (request.META['HTTP_HOST']))
        # if self.utils.is_local(request.META['HTTP_HOST']):
        #     root_dir  = C.output_root_mbl_local

        self.output_dir = os.path.join(root_dir, platform, id_number)    
        if (lane_name != ''):
            self.output_dir = os.path.join(root_dir, platform, id_number, lane_name)

class Run():
    def __init__(self):
        self.utils = Utils()
        self.all_suites = models_l_env454.RunInfoIll.cache_all_method.select_related('run', 'primer_suite')
        self.run_data = {}

    def get_primer_suites(self, run, lane, suite_domain):
        # all_suites = RunInfoIll.objects.filter(run__run = run, lane = lane)
        try:
            all_suites = self.all_suites.filter(run__run = run, lane = lane)
            primer_suites = set([entry.primer_suite for entry in all_suites if entry.primer_suite.primer_suite.startswith(suite_domain)])
            return (True, next(iter(primer_suites)).primer_suite)
        except StopIteration:
            error_message = "There is no such combination in our database: run = %s, lane = %s, and domain = %s" % (run, lane, suite_domain)
            return (False, error_message)
        except ValueError:
            error_message = "The lane number you entered is not valid: lane = %s" % (lane)
            return (False, error_message)
        except:
            raise

    def get_run(self, request):
        logging.info("Running get_run from utils")
        error_message = ""

        if request.method == 'POST':
            form = RunForm(request.POST)
            # logging.info("request.POST = ")
            # print request.POST
            if form.is_valid():
                self.run_data['find_rundate'] = form.cleaned_data['find_rundate'].run
                self.run_data['find_machine'] = form.cleaned_data['find_machine']
                self.run_data['find_domain']  = form.cleaned_data['find_domain']
                self.run_data['find_lane']    = form.cleaned_data['find_lane']
                self.run_data['full_machine_name'] = self.utils.get_full_macine_name(form.cleaned_data['find_machine'])
                self.run_data['perfect_overlap']   = self.utils.get_overlap(form.cleaned_data['find_machine'])
                suite_domain                  = self.utils.get_domain_name(form.cleaned_data['find_domain'])
                primer_suite = self.get_primer_suites(self.run_data['find_rundate'], self.run_data['find_lane'], suite_domain)
                # logging.info("primer_suite[1]")
                #
                # print primer_suite[1]

                if (primer_suite[0]):
                    self.run_data['primer_suite'] = primer_suite[1]
                else:
                    error_message = primer_suite[1]
                    self.run_data['primer_suite'] = ""
                
                request.session['run_form_data'] = self.run_data
                
        elif request.session['run_form_data']:
            form = RunForm(request.session['run_form_data'])
            
            print "request.session['run_form_data'] = "
            print request.session['run_form_data']
        
            self.run_data = request.session['run_form_data']
            print "EEE self.run_data['find_rundate']"
            print self.run_data['find_rundate']

            print "self.run_data['full_machine_name']"
            print self.run_data['full_machine_name']

            try:
                self.run_data['find_rundate'] = models_l_env454.Run.cache_all_method.get(run = self.run_data['find_rundate'], platform = self.run_data['full_machine_name']).pk
            except models_l_env454.Run.DoesNotExist:
                form = RunForm()
            
        
        # if a GET (or any other method) we'll create a blank form
        else:
            try:
                self.get_run_data_from_session(request)
                logging.debug("self.run_data['find_rundate'] = %s" % self.run_data['find_rundate'])
                rundate_id = models_l_env454.Run.cache_all_method.get(run = self.run_data['find_rundate'], platform = self.run_data['full_machine_name']).pk
                init_run_data = self.run_data.copy()
                init_run_data.update({'find_rundate': rundate_id})
                form = RunForm(initial = init_run_data)
                
            except KeyError:
                form = RunForm()
            except models_l_env454.Run.DoesNotExist:
                form = RunForm()
            except:
                raise
            
        return (form, self.run_data, error_message)
        
        """
        'run_form_data'
	
        {'find_domain': u'B',
         'find_lane': u'1',
         'find_machine': u'hs',
         'find_rundate': u'20160504',
         'full_machine_name': 'hiseq',
         'perfect_overlap': 'True',
         'primer_suite': u'Bacterial V4-V5 Suite'}
            
        
        """
        
    def get_run_data_from_session(self, request):

        # print "request.session['out_metadata']"
        # print request.session['out_metadata']
        
        lanes_domains = self.utils.get_lanes_domains(request.session['out_metadata'])
        random_lane_domain = lanes_domains[0].split("_")
    
        self.run_data['find_rundate']      = request.session['run_info']['selected_rundate']
        self.run_data['find_machine']      = request.session['run_info']['selected_machine_short']
        self.run_data['find_domain']       = random_lane_domain[1]
        self.run_data['find_lane']         = random_lane_domain[0]
        self.run_data['full_machine_name'] = request.session['run_info']['selected_machine']
        self.run_data['perfect_overlap']   = self.utils.get_overlap(request.session['run_info']['selected_machine_short'])
        suite_domain                  = self.utils.get_domain_name(self.run_data['find_domain'])
        primer_suite = self.get_primer_suites(self.run_data['find_rundate'], self.run_data['find_lane'], suite_domain)
    
        # print "self.run_data from out_metadata"
        # print self.out_metadata
        

    