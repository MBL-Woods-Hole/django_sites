from .forms import RunForm, FileUploadForm, CsvRunInfoUploadForm
from .model_choices import *
from .models_l_env454 import RunInfoIll, Run as model_run
# import models_l_env454

import time
import os
import logging
import stat
import subprocess

class Utils():

    def benchmark_w_return_1(self):
        logging.info("\n")
        logging.info("-" * 10)
        return time.time()

    def benchmark_w_return_2(self, t0):
        t1 = time.time()
        total = float(t1-t0) / 60
        # print 'time: %.2f m' % total
        # print 'time: %f s' % total
        logging.info('time: %f s' % total)
        

    def is_local(self, request):
        local_hostnames = ["127.0.0.1", "localhost"]
        hostname = request.get_host()
        if hostname.startswith(tuple(local_hostnames)):
            return True
        else:
            return False

    def get_overlap(self, machine_name):
        overlap_choices = dict(Overlap.COMPLETE_OVERLAP_CHOICES)
        return overlap_choices[machine_name]

    def get_full_macine_name(self, machine_name):
        machine_choices = dict(Machine.MACHINE_CHOICES)
        return machine_choices[machine_name]

    def get_domain_name(self, domain_name):
        domain_choices = dict(Domain.SUITE_DOMAIN_CHOICES)
        return domain_choices[domain_name]

    def clear_session(self, request):
        try:
            key_list = list(request.session.keys())
            for key in key_list:
                del request.session[key]
                # continue
            # for key in list(request.session):
            #     del request.session[key]
        except KeyError:
            pass
        except AttributeError:
            key_list = []

            
    # TODO: combine with metadata_utils, DRY!
    def get_lanes_domains(self, out_metadata):
        domain_choices = dict(Domain.LETTER_BY_DOMAIN_CHOICES)
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
        
    def chmod_wg(self, curr_name):
        st = os.stat(curr_name)
        try:
            os.chmod(curr_name, st.st_mode | stat.S_IWGRP)
        except OSError:
            logging.warning("Can't change permissions for %s " % (curr_name))
        except:
            raise

    def check_and_make_dir(self, dir_name):
        try:
            os.makedirs(dir_name)
            self.chmod_wg(dir_name)

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
        self.all_suites = RunInfoIll.cache_all_method.select_related('run', 'primer_suite')
        self.run_data = {}
        self.db_info = {'env454': 'bpcdb1', 'vamps2': 'vampsdb'}

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

    def get_current_primer_suite(self, find_domain):
        suite_domain = self.utils.get_domain_name(find_domain)
        return self.get_primer_suites(self.run_data['find_rundate'], self.run_data['find_lane'], suite_domain)

    def get_run(self, request):
        logging.info("Running get_run from utils")
        error_message = ""

        if request.method == 'POST':
            form = RunForm(request.POST)
            # logging.info("request.POST = ")
            # print request.POST
            if form.is_valid():
                self.run_data.update(form.cleaned_data)
                self.run_data['find_rundate'] = form.cleaned_data['find_rundate'].run
                self.run_data['full_machine_name'] = self.utils.get_full_macine_name(form.cleaned_data['find_machine'])
                self.run_data['perfect_overlap']   = self.utils.get_overlap(form.cleaned_data['find_machine'])
                self.run_data['rundate_dir']       = self.calculate_rundate_dir(self.run_data['find_rundate'])
                self.run_data['db_host']      = self.db_info[self.run_data['find_db_name']]

                primer_suite = self.get_current_primer_suite(form.cleaned_data['find_domain'])

                if (primer_suite[0]):
                    self.run_data['primer_suite'] = primer_suite[1]
                else:
                    error_message = primer_suite[1]
                    self.run_data['primer_suite'] = ""

                try:
                    del request.session['run_form_data']
                except KeyError:
                    pass
                except:
                    raise
                request.session['run_form_data'] = self.run_data
               
        else:    
            try:
                if request.session['run_form_data']:
                    self.run_data = request.session['run_form_data']
                else:
                    self.get_run_data_from_session(request)

                rundate_id = model_run.cache_all_method.get(run = self.run_data['find_rundate'], platform = self.run_data['full_machine_name']).pk
                self.run_data['rundate_dir'] = self.calculate_rundate_dir(self.run_data['find_rundate'])

                init_run_data = self.run_data.copy()
                init_run_data.update({'find_rundate': rundate_id})

                form = RunForm(initial = init_run_data)        
            except KeyError:
                form = RunForm()
            except model_run.DoesNotExist:
                form = RunForm()
            except:
                raise
            
        return (form, self.run_data, error_message)
        
    def get_run_data_from_session(self, request):

        # print "request.session['out_metadata']"
        # print request.session['out_metadata']
        
        lanes_domains = self.utils.get_lanes_domains(request.session['out_metadata'])
        random_lane_domain = lanes_domains[0].split("_")

        self.run_data.update(request.session['run_info'])
        self.run_data['find_rundate']      = request.session['run_info']['selected_rundate']
        self.run_data['find_machine']      = request.session['run_info']['selected_machine_short']
        self.run_data['find_domain']       = random_lane_domain[1]
        self.run_data['find_lane']         = random_lane_domain[0]
        self.run_data['full_machine_name'] = request.session['run_info']['selected_machine']
        self.run_data['perfect_overlap']   = self.utils.get_overlap(request.session['run_info']['selected_machine_short'])
        primer_suite = self.get_current_primer_suite(self.run_data['find_domain'])
        # self.run_data['find_db_name'] = request.session['run_info']['find_db_name']
        self.run_data['db_host'] = self.db_info[self.run_data['find_db_name']]

        # print "self.run_data from out_metadata"
        # print self.out_metadata
        

    def calculate_rundate_dir(self, rundate):
        year = str(rundate)[0:4]
        if int(year) < 2017:
            return "runs_%s/" % year
        else:
            return ""