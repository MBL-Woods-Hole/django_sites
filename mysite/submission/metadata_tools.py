from __future__ import unicode_literals
from .forms import RunForm, FileUploadForm, CsvRunInfoUploadForm, MetadataOutCsvForm, AddProjectForm
from .utils import Utils, Dirs
from collections import defaultdict
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.db import connections
from django.db.models import Q
from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
import codecs
import csv
from .model_choices import Overlap, Machine, Domain
from .models_l_env454 import *
from .models_l_vamps import *
import os
import stat
import time
import logging

# Assuming that in each csv one rundate and one platform!
class CsvMetadata():
    """
    IN
    Unique per upload (run_info):
        Run date:
        Path to raw data:
        Platform:
        DNA Region:
        Overlap:
        Has Ns:
        Seq Operator:
        Insert Size:
        Read Length:

    Can be changed in the table:
        HEADERS_TO_EDIT_METADATA

    Taken from csv: HEADERS_FROM_CSV
    Taken from vamps_submission tables on vamps:
        'vamps_auth_id'
        'first_name'
        'project_description'
        'funding'
        'institution'
        'title'
        'num_of_tubes'
        'date_initial'
        'submit_code'
        'email'
        'date_updated'
        'last_name'
        'temp_project'
        'user'
        'passwd'
        'security_level'
        'active'
        'locked'
        'date_added'
        'id'
    Taken from user table on env454:
        see models

    OUT:
    ini:
        "rundate"
        "lane_domain"
        "dna_region"
        "path_to_raw_data"
        "overlap"
        "machine"
    csv: HEADERS_TO_CSV
    """

    def __init__(self, request):

        self.utils = Utils()
        self.db_prefix = ""
        logging.info("self.utils.is_local(request) = %s" % self.utils.is_local(request))
        if (self.utils.is_local(request)):
            self.db_prefix = "test_"
        
        self.RUN_INFO_FORM_FIELD_HEADERS = ["dna_region", "insert_size", "op_seq", "overlap", "read_length", "rundate"]
        self.csv_headers = []
        self.csv_content = []
        self.run_info_from_csv = {}
        self.errors = []
        self.csv_by_header_uniqued = defaultdict(list)
        self.csv_by_header = defaultdict(list)
        self.csvfile = ""
        self.cause = ""
        self.path_to_csv = ""
        self.selected_lane = ""
        self.domain_letter = ""
        self.selected_machine_short = ""
        self.ini_names = {}
        self.metadata_csv_file_names = {}
        self.dirs = Dirs()
        self.lanes_domains = []
        # self.out_metadata = defaultdict(lambda: defaultdict(int))
        self.out_metadata = defaultdict(defaultdict)
        self.out_metadata_table = defaultdict(list)
        self.vamps_submissions = {}
        self.user_info_arr = {}
        self.adaptors_full = {}
        self.domain_choices = dict(Domain.LETTER_BY_DOMAIN_CHOICES)
        self.machine_shortcuts_choices = dict(Machine.MACHINE_SHORTCUTS_CHOICES)
        self.files_created = []
        self.empty_cells = []
        self.new_project = ""
        self.new_project_created = False
        self.adaptor_ref = self.get_all_adaptors()
        
        self.HEADERS_FROM_CSV = {
            'id': {'field': 'id', 'required': True},
            'submit_code': {'field': 'submit_code', 'required': True},
            'user': {'field': 'user', 'required': True},
            'tube_number': {'field': 'tube_number', 'required': True},
            'tube_label': {'field': 'tube_label', 'required': False},
            'dataset_description': {'field': 'dataset_description', 'required': False},
            'duplicate': {'field': 'duplicate', 'required': False},
            'domain': {'field': 'domain', 'required': True},
            'primer_suite': {'field': 'primer_suite', 'required': True},
            'dna_region': {'field': 'dna_region', 'required': True},
            'project_name': {'field': 'project_name', 'required': True},
            'dataset_name': {'field': 'dataset_name', 'required': True},
            'runkey': {'field': 'runkey', 'required': False},
            'barcode': {'field': 'barcode', 'required': False},
            'pool': {'field': 'pool', 'required': False},
            'lane': {'field': 'lane', 'required': True},
            'direction': {'field': 'direction', 'required': False},
            'platform': {'field': 'platform', 'required': True},
            'op_amp': {'field': 'op_amp', 'required': True},
            'op_seq': {'field': 'op_seq', 'required': True},
            'op_empcr': {'field': 'op_empcr', 'required': False},
            'enzyme': {'field': 'enzyme', 'required': False},
            'rundate': {'field': 'rundate', 'required': True},
            'adaptor': {'field': 'adaptor', 'required': True},
            'date_initial': {'field': 'date_initial', 'required': True},
            'date_updated': {'field': 'date_updated', 'required': True},
            'on_vamps': {'field': 'on_vamps', 'required': False},
            'sample_received': {'field': 'sample_received', 'required': False},
            'concentration': {'field': 'concentration', 'required': True},
            'quant_method': {'field': 'quant_method', 'required': True},
            'overlap': {'field': 'overlap', 'required': True},
            'insert_size': {'field': 'insert_size', 'required': True},
            'barcode_index': {'field': 'barcode_index', 'required': False},
            'read_length': {'field': 'read_length', 'required': True},
            'trim_distal': {'field': 'trim_distal', 'required': False},
            'env_sample_source_id': {'field': 'env_sample_source_id', 'required': True},
        }

        self.HEADERS_TO_CSV = ['adaptor', 'amp_operator', 'barcode', 'barcode_index', 'data_owner', 'dataset', 'dataset_description', 'dna_region', 'email', 'env_sample_source_id', 'first_name', 'funding', 'insert_size', 'institution', 'lane', 'last_name', 'overlap', 'platform', 'primer_suite', 'project', 'project_description', 'project_title', 'read_length', 'run', 'run_key', 'seq_operator', 'tubelabel']

        self.HEADERS_TO_EDIT_METADATA = ['domain', 'lane', 'contact_name', 'run_key', 'barcode_index', 'adaptor', 'project', 'dataset', 'dataset_description', 'env_source_name', 'tubelabel', 'barcode', 'amp_operator']

        self.required_headers = [header_name for header_name, values in
                                 self.HEADERS_FROM_CSV.items() if values['required']]
        # logging.debug("self.required_headers = %s" % self.required_headers)

    def no_data_message(self):
        return 'There is no data for <span class="emph_it">%s</span> in the file <span class="emph_it">%s</span>' % (self.cause, self.csvfile)

    def import_from_file(self, csvfile):
        logging.info("import_from_file")
        
        self.csvfile = csvfile
        dialect = self.get_dialect()

        self.get_reader(dialect)
        self.csv_headers, self.csv_content = self.parce_csv()

        self.csvfile.seek(0)
        for r in self.reader:
            print("PPP parce_csv row")
            print(r)
        next(self.reader)

        self.check_headers_presence()
        self.check_req_info_presence()

        if len(self.empty_cells) > 0:
            return len(self.empty_cells)
        else:
            self.get_csv_by_header_uniqued()
            return 0

    def get_dialect(self):
        try:
            open_file = codecs.EncodedFile(self.csvfile, "utf-8")
            open_file_part = open_file.read(1024).decode("utf-8")
            # dialect = csv.Sniffer().sniff(codecs.EncodedFile(self.csvfile, "utf-8").read(1024), delimiters=',')
            dialect = csv.Sniffer().sniff(open_file_part, delimiters=',')
        except csv.Error as e:
            logging.warning("Warning for %s: %s' % (self.csvfile, e)")
            pass
            # self.errors.append('Warning for %s: %s' % (self.csvfile, e))
        except:
            raise
        else:
            if dialect:
              self.csvfile.seek(0)
              logging.info("dialect.delimiter")
              logging.info(dialect.delimiter)
              # logging.info(dir(dialect))
              # ['__doc__', '__init__', '__module__', '_name', '_valid', '_validate', 'delimiter', 'doublequote', 'escapechar', 'lineterminator', 'quotechar', 'quoting', 'skipinitialspace']

              # logging.info("----")
              return dialect
            else:
              logging.warning("WARNING, file %s is empty (size = %s), check it's path" % (self.csvfile.name, self.csvfile.size))

    def get_reader(self, dialect):
        try:
            # open_file = codecs.EncodedFile(self.csvfile, "utf-8")
            # open_file_part = open_file.read().decode("utf-8")

            # open_file = codecs.EncodedFile(self.csvfile, "utf-8")
            # open_file_part = open_file.read().decode("utf-8")
            # self.csvfile.open()
            # self.reader = csv.reader(codecs.EncodedFile(self.csvfile, "utf-8"), delimiter=',', dialect=dialect)
            # param_file = self.csvfile.read()
            # self.reader = csv.reader(open_file, delimiter=',', dialect=dialect)

            csvfile = csv.reader(codecs.iterdecode(self.csvfile, 'utf-8'))
            for line in csvfile:
                print("LLL LINE")  # do something with line
                print(line)  # do something with line


        except csv.Error as e:
            self.errors.append('%s is not a valid CSV file: %s' % (self.csvfile, e))
        except:
            raise

    def get_csv_by_header(self):
        for row in zip(*self.csv_content):
            self.csv_by_header[row[0]] = row[1:]

    def get_csv_by_header_uniqued(self):
        self.csv_by_header_uniqued = ""
        self.csv_by_header_uniqued = dict((x[0], list(set(x[1:]))) for x in zip(*self.csv_content))

    def get_initial_run_info_data_dict(self):
        logging.info("get_initial_run_info_data_dict")
        
        try:
            csv_rundate = "".join(self.csv_by_header_uniqued['rundate'])

            
            platform = "".join(self.csv_by_header_uniqued['platform'])
            self.selected_machine_short = self.machine_shortcuts_choices[platform]
            
            self.run_info_from_csv = {
                'csv_rundate':          csv_rundate,
                'csv_path_to_raw_data': "/xraid2-2/sequencing/Illumina/%s%s" % (csv_rundate, self.selected_machine_short),
                'csv_platform':	        platform,
                'csv_dna_region':	    "".join(self.csv_by_header_uniqued['dna_region']),
                'csv_overlap':		    "".join(self.csv_by_header_uniqued['overlap']),
                'csv_has_ns':		    "".join(self.csv_by_header_uniqued['rundate']),
                'csv_seq_operator':	    "".join(self.csv_by_header_uniqued['op_seq']),
                'csv_insert_size':	    "".join(self.csv_by_header_uniqued['insert_size']),
                'csv_read_length':	    "".join(self.csv_by_header_uniqued['read_length'])
            }

            # logging.debug("RRR self.run_info_from_csv"
            # logging.debug(self.run_info_from_csv)
        except KeyError as e:
            self.cause = e.args[0]
            self.errors.append(self.no_data_message())
        except:
            raise

    def parce_csv(self):
      for r in self.reader:
          print("PPP parce_csv row")
          print(r)
          # read().decode('utf-8')


      for y_index, row in enumerate(self.reader):
          print("parce_csv row")
          print(row)

          self.csv_content.append(row)
          if y_index == 0:
              self.csv_headers = [header_name.lower() for header_name in row if header_name]
              continue
      return self.csv_headers, self.csv_content

    def check_headers_presence(self):
      missing_headers = set(self.required_headers) - set([r.lower() for r in self.csv_headers])
      # logging.debug("self.csv_headers = " )
      # logging.debug(self.csv_headers)
      if missing_headers:
          missing_headers_str = ', '.join(missing_headers)
          self.errors.append('Missing headers: %s' % (missing_headers_str))
          # logging.debug("self.errors 3")
          # logging.debug(self.errors)
          # raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
          return False
      return True

    def check_req_info_presence(self):
        empty_cells_interim = []
        for row in self.reader:
            for header in self.csv_headers:
                if header in self.required_headers:
                    ind = self.csv_headers.index(header)
                    # logging.debug("header = %s; row[ind] = %s" % (header, row[ind])
                    if not row[ind]:
                        empty_cells_interim.append(header)
                        # logging.debug("NOOOO")
        self.empty_cells = list(set(empty_cells_interim))

    def run_query_to_dict(self, query):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        
        res_dict = {}
        # print "111 connections"
        # for k, v in connections.items():
        #   pp.pprint("k = %s, v = %s") % (k,v)
        #
        # print "222 connection"
        # print connection.values()
        
        cursor = connections['vamps'].cursor()
        # cursor = connection.cursor()
        cursor.execute(query)

        column_names = [d[0] for d in cursor.description]

        for row in cursor:
          res_dict = dict(zip(column_names, row))

        return res_dict
      # dump it to a json string
      # self.vamps_submissions = json.dumps(info)

    def get_vamps_submission_info(self):
        db_name = self.db_prefix + "vamps"
        
        # out_file_name = "temp_subm_info"
        try:
            for submit_code in self.csv_by_header_uniqued['submit_code']:
                query_subm = """SELECT subm.*, auth.user, auth.passwd, auth.first_name, auth.last_name, auth.active, auth.security_level, auth.email, auth.institution, auth.date_added
                    FROM %s.vamps_submissions AS subm
                    JOIN %s.vamps_auth AS auth
                      ON (auth.id = subm.vamps_auth_id)
                    WHERE submit_code = \"%s\"""" % (db_name, db_name, submit_code)
                self.vamps_submissions[submit_code] = self.run_query_to_dict(query_subm)
        except KeyError as e:
            self.cause = e.args[0]
            self.errors.append(self.no_data_message())
        except:
            raise

    # def benchmark_w_return_1(self):
    #   logging.debug("\n")
    #   logging.debug("-" * 10)
    #   return time.time()
    #
    # def benchmark_w_return_2(self, t0):
    #   t1 = time.time()
    #   total = float(t1-t0) / 60
    #   logging.debug('time: %.2f m' % total)

    def get_adaptor_from_csv_content(self):
        for i in xrange(len(self.csv_content)-1):
            # logging.debug("+" * 9)
            adaptor    = self.csv_by_header['adaptor'][i]
            dna_region = self.csv_by_header['dna_region'][i]
            domain     = self.csv_by_header['domain'][i]

            self.get_adaptors_full(adaptor, dna_region, domain)

    def get_all_adaptors(self):
        db_name = self.db_prefix + "env454"
        return IlluminaAdaptorRef.cache_all_method.select_related('illumina_adaptor', 'illumina_index', 'illumina_run_key', 'dna_region')

    def get_adaptors_full(self, adaptor, dna_region, domain):
        db_name = self.db_prefix + "env454"
        # self.adaptor_ref
        # links = IlluminaAdaptorRef.cache_all_method.select_related('illumina_adaptor', 'illumina_index', 'illumina_run_key', 'dna_region')
        # logging.debug(links.filter(Q(illumina_adaptor_id__illumina_adaptor = "A04") | Q(illumina_adaptor_id__illumina_adaptor = "A08")))
        
        key = "_".join([adaptor, dna_region, domain])
        mm = self.adaptor_ref.filter(illumina_adaptor_id__illumina_adaptor = adaptor).filter(dna_region_id__dna_region = dna_region).filter(domain = domain)
                
        # TODO: make once self.adaptors_full.update({})
        
        # logging.debug("self.adaptors_full timing 2")
        # t0 = self.utils.benchmark_w_return_1()
        self.adaptors_full = {key: (row.illumina_index, row.illumina_run_key) for row in mm}
        # self.utils.benchmark_w_return_2(t0)


    def get_user_name_by_submit_code(self, submit_code):
      submit_code_idx = self.csv_content[0].index("submit_code")
      user_name_idx   = self.csv_content[0].index("user")
      user_name_by_submit_code = ""

      for sublist in self.csv_content:
         if sublist[submit_code_idx] == submit_code:
             user_name_by_submit_code = sublist[user_name_idx]
             break
      return user_name_by_submit_code


    def get_user_info(self):
        db_name = self.db_prefix + "env454"

        try:
            # TODO: collect submit_code and vamps_user_id into a dict, run one query with "OR"
            for submit_code in self.csv_by_header_uniqued['submit_code']:
                # logging.debug("submit_code = %s, self.vamps_submissions[submit_code]['user'] = %s" % (submit_code, self.vamps_submissions[submit_code]['user']))
                try:
                  vamps_user_id = self.vamps_submissions[submit_code]['user']
                except KeyError as e:
                  user_name_by_submit_code = self.get_user_name_by_submit_code(submit_code)
                  self.errors.append("Please check if contact information for %s exists in VAMPS." % user_name_by_submit_code)
                  return                    
                except:
                  raise

                try:
                    contacts = Contact.cache_all_method.get(vamps_name = vamps_user_id)
                except Contact.DoesNotExist as e:
                    # self.cause = e.args[0]
                    self.errors.append("Please add contact information for %s to env454." % vamps_user_id)
                except:
                    raise

                # .filter(vamps_name = vamps_user_id)

                # logging.debug("CCC contacts = %s" % contacts)

                # for row in contacts:
                self.user_info_arr[submit_code] = model_to_dict(contacts)

                # self.user_info_arr.append({submit_code: (model_to_dict(row)) for row in contacts})

            # logging.debug("self.user_info_arr = %s" % self.user_info_arr)
        # except KeyError as e:
        #     self.cause = e.args[0]
        #     print "self.cause SSS" 
        #     print self.cause
        #     
        #     self.errors.append(self.no_data_message())
        #     self.errors.append(" Or the vamps_submission table has no such submit_code.")
        except:
            raise

    def get_selected_variables(self, request_post):
        # change from form if needed
        # machine_shortcuts_choices = dict(Machine.MACHINE_SHORTCUTS_CHOICES)

        if 'submit_run_info' in request_post:
            self.selected_machine       = request_post.get('csv_platform', False)
            # logging.debug("self.selected_machine in request_post= %s" % (self.selected_machine))
            self.selected_machine_short = self.machine_shortcuts_choices[self.selected_machine]
            self.selected_rundate       = request_post.get('csv_rundate', False)
            self.selected_dna_region    = request_post.get('csv_dna_region', False)
            self.selected_overlap       = request_post.get('csv_overlap', False)
        else:
            # logging.debug("self.csv_by_header_uniqued['platform']")
            # logging.debug(self.csv_by_header_uniqued['platform'])
            self.selected_machine = " ".join(self.csv_by_header_uniqued['platform']).lower()
            # logging.debug("self.selected_machine 2 = %s" % self.selected_machine)
            # logging.debug("MMM self.machine_shortcuts_choices")
            # logging.debug(self.machine_shortcuts_choices)
            self.selected_machine_short = self.machine_shortcuts_choices[self.selected_machine]
            # logging.debug("self.selected_machine_short 2 = %s" % self.selected_machine_short)

            self.selected_rundate = " ".join(self.csv_by_header_uniqued['rundate']).lower()

    def create_path_to_csv(self):
        # /xraid2-2/g454/run_new_pipeline/illumina/miseq_info/20160711
        # logging.debug("self.selected_machine from create_path_to_csv = %s" % (self.selected_machine))

        self.path_to_csv = os.path.join(settings.ILLUMINA_RES_DIR, self.selected_machine + "_info", self.selected_rundate)
        logging.debug("self.path_to_csv")
        logging.debug(self.path_to_csv)
        new_dir = self.dirs.check_and_make_dir(self.path_to_csv)

    def create_out_file_names(self, pattern):
        return {lane_domain: pattern % (self.selected_rundate, self.selected_machine_short, lane_domain) for lane_domain in self.lanes_domains}

    def create_ini_names(self):
        self.ini_names = self.create_out_file_names("%s_%s_%s_run_info.ini")

    def make_out_metadata_csv_file_names(self):
        # OLD: metadata_20160803_1_B.csv
        # NEW: metadata_20151111_hs_1_A.csv
        self.metadata_csv_file_names = self.create_out_file_names("metadata_%s_%s_%s.csv")

    def write_ini(self):
        path_to_raw_data = "/xraid2-2/sequencing/Illumina/%s%s/" % (self.selected_rundate, self.selected_machine_short)
        overlap_choices = dict(Overlap.OVERLAP_CHOICES)

        for lane_domain, ini_name in self.ini_names.items():
            ini_text = '''{"rundate":"%s","lane_domain":"%s","dna_region":"%s","path_to_raw_data":"%s","overlap":"%s","machine":"%s"}
                        ''' % (self.selected_rundate, lane_domain, self.selected_dna_region, path_to_raw_data, overlap_choices[self.selected_overlap], self.selected_machine)
            full_ini_name = os.path.join(self.path_to_csv, ini_name)
            ini_file = open(full_ini_name, 'w')
            ini_file.write(ini_text)
            ini_file.close()
            self.dirs.chmod_wg(full_ini_name)
            

    def write_out_metadata_to_csv(self, my_post_dict, request):
        logging.info("write_out_metadata_to_csv")
        
        writers = {}
        for lane_domain in self.metadata_csv_file_names.keys():
            # writers[lane_domain] = csv.DictWriter(open(os.path.join(self.path_to_csv, self.metadata_csv_file_names[lane_domain]), 'ab'), self.HEADERS_TO_CSV)
            writers[lane_domain] = csv.DictWriter(open(os.path.join(self.path_to_csv, self.metadata_csv_file_names[lane_domain]), 'w'), self.HEADERS_TO_CSV)
            writers[lane_domain].writeheader()
        
        for idx, val in self.out_metadata.items():
            # todo: DRY
            domain_letter = self.domain_choices[val['domain']]
            lane_domain = "%s_%s" % (val['lane'], domain_letter)
            # for h in self.HEADERS_TO_CSV:
            #     logging.debug("TTT idx = %s, val = %s, h = %s, val[h] = %s" % (idx, val, h, val[h]))

            to_write = {h: val[h] for h in self.HEADERS_TO_CSV}
                
            writers[lane_domain].writerow(to_write)

    def check_out_csv_files(self):
        for lane_domain, file_name in self.metadata_csv_file_names.items():
            if os.path.isfile(os.path.join(self.path_to_csv, file_name)):
                curr_file = os.path.join(self.path_to_csv, file_name)
                self.files_created.append(curr_file)
                self.dirs.chmod_wg(curr_file)

    def update_out_metadata(self, my_post_dict, request):
        logging.info("update_out_metadata")

        # ???
        for header in self.HEADERS_TO_CSV:
            for i in self.out_metadata.keys():
                try:
                    self.out_metadata[i][header] = my_post_dict['form-' + str(i) + '-' + header]
                except MultiValueDictKeyError as e:
                    pass
                except:
                    raise

    def edit_out_metadata(self, request):
        logging.info("edit_out_metadata")

        try:
            self.out_metadata = request.session['out_metadata']
        except KeyError:
            request.session['out_metadata'] = self.out_metadata
        except:
            raise
        
        # logging.debug("FROM edit_out_metadata: request.session['out_metadata']")
        # logging.debug(request.session['out_metadata'])
        

        for i, v in self.out_metadata.items():
            # logging.debug("i = %s" % i)
            self.out_metadata[i]['dna_region']		    = request.POST.get('csv_dna_region', False)
            self.out_metadata[i]['has_ns']			    = request.POST.get('csv_has_ns', False)
            self.out_metadata[i]['insert_size']		    = request.POST.get('csv_insert_size', False)
            self.out_metadata[i]['overlap']			    = request.POST.get('csv_overlap', False)
            self.out_metadata[i]['path_to_raw_data']	= request.POST.get('csv_path_to_raw_data', False)
            self.out_metadata[i]['platform']			= request.POST.get('csv_platform', False)
            self.out_metadata[i]['read_length']			= request.POST.get('csv_read_length', False)
            self.out_metadata[i]['run']				    = request.POST.get('csv_rundate', False)
            self.out_metadata[i]['seq_operator']		= request.POST.get('csv_seq_operator', False)

            # TODO:
            # ? 'overlap': 'hs_complete' now!

        # logging.debug("self.out_metadata = %s" % self.out_metadata)

    def edit_out_metadata_table(self, request):
        logging.info("edit_out_metadata_table")
        
        self.out_metadata_table = request.session['out_metadata_table']

        # logging.debug("OOO request.session['run_info_form_post']['csv_has_ns']")
        # logging.debug(request.session['run_info_form_post']['csv_has_ns'])

        for x in range(0, len(self.out_metadata_table['rows'])):
            adaptor    = request.POST['form-'+str(x)+'-adaptor']
            dna_region = request.session['run_info_form_post']['csv_dna_region']
            domain     = request.POST['form-'+str(x)+'-domain']

            key = "_".join([adaptor, dna_region, domain])

            self.get_adaptors_full(adaptor, dna_region, domain)
            # nnnn = ""
            
            try:
                self.out_metadata_table['rows'][x]['barcode_index'] = self.adaptors_full[key][0].illumina_index
                # if (request.session['run_info_form_post']['csv_has_ns'] == 'yes'):
                #     nnnn = "NNNN"
                # self.out_metadata_table['rows'][x]['run_key']       = nnnn + self.adaptors_full[key][1].illumina_run_key
                self.out_metadata_table['rows'][x]['run_key']       = self.adaptors_full[key][1].illumina_run_key
            except KeyError:
                self.out_metadata_table['rows'][x]['barcode_index'] = ""
                self.out_metadata_table['rows'][x]['run_key']       = ""
            except:
                raise

    def add_out_metadata_table_to_out_metadata(self, request):
        logging.info("add_out_metadata_table_to_out_metadata")
        
        nnnn = ""
        # TODO: benchmark
        for x in range(0, len(request.session['out_metadata_table']['rows'])):
            # logging.debug("SSS1 self.out_metadata_table['rows'][x]['run_key']")
            # logging.debug(self.out_metadata_table['rows'][x]['run_key'])
            for header in self.HEADERS_TO_EDIT_METADATA:
                if (self.out_metadata_table['rows'][x][header] != request.POST['form-'+str(x)+'-' + header]):
                    self.out_metadata_table['rows'][x][header] = request.POST['form-'+str(x)+'-' + header]
                    
            if (request.session['run_info_form_post']['csv_has_ns'] == 'yes') and not self.out_metadata_table['rows'][x]['run_key'].startswith("NNNN"):
                nnnn = "NNNN"
            self.out_metadata_table['rows'][x]['run_key'] = nnnn + request.POST['form-'+str(x)+'-' + 'run_key']

            # logging.debug("SSS2 self.out_metadata_table['rows'][x]['run_key']")
            # logging.debug(self.out_metadata_table['rows'][x]['run_key'])
                    

    def edit_post_metadata_table(self, request):
        logging.info("edit_post_metadata_table")
        
        my_post_dict = request.POST.copy()
        my_post_dict['form-TOTAL_FORMS']   = len(request.session['out_metadata'].keys())
        my_post_dict['form-INITIAL_FORMS'] = len(request.session['out_metadata'].keys())
        my_post_dict['form-MAX_NUM_FORMS'] = len(request.session['out_metadata_table'].keys())
        
        
        nnnn = ""
        for x in range(0, len(request.session['out_metadata_table']['rows'])):
            # logging.debug("SSS3 self.out_metadata_table['rows'][x]['run_key']")
            # logging.debug(self.out_metadata_table['rows'][x]['run_key'])
            my_post_dict['form-'+str(x)+'-barcode_index'] = self.out_metadata_table['rows'][x]['barcode_index']
            if (request.session['run_info_form_post']['csv_has_ns'] == 'yes') and not self.out_metadata_table['rows'][x]['run_key'].startswith("NNNN"):
                nnnn = "NNNN"
            my_post_dict['form-'+str(x)+'-run_key']       = nnnn + self.out_metadata_table['rows'][x]['run_key']
            
            # logging.debug("SSS4 self.out_metadata_table['rows'][x]['run_key']")
            # logging.debug(self.out_metadata_table['rows'][x]['run_key'])
                                
        return my_post_dict
        
    def check_projects(self):
      missing_projects = []
      for i in xrange(len(self.csv_content)-1):
        try:
          csv_project = self.csv_by_header['project_name'][i]
          db_project = Project.objects.get(project=csv_project)
        except Project.DoesNotExist as e:
          missing_projects.append(csv_project)
        except:
          raise
          
      missing_projects_list = ", ".join(list(set(missing_projects)))
      if len(missing_projects_list) > 0:
        self.errors.append("Please add project information for %s to env454." % missing_projects_list)

    def make_new_out_metadata(self):
        logging.info("make_new_out_metadata")
        idx = 0
        # logging.debug("self.csv_content = %s, len(self.csv_content) = %s" % (self.csv_content, len(self.csv_content)))
        # logging.debug("self.csv_content[0] =  head = %s" % (self.csv_content[0]))

        # logging.debug(" &&&&&&& list(set(self.csv_content[0]) & set(self.HEADERS_TO_CSV))")
        # a = list(set(self.csv_content[0]) & set(self.HEADERS_TO_CSV))
        # logging.debug(a)
        # ['barcode_index', 'lane', 'dna_region', 'read_length', 'env_sample_source_id', 'barcode', 'overlap', 'dataset_description', 'adaptor', 'primer_suite', 'insert_size']

        # logging.debug("self.csv_by_header = %s" % self.csv_by_header)

        # logging.debug("UUU self.adaptors_full = %s" % self.adaptors_full)
        # {'A08_v4v5_bacteria': (<IlluminaIndex: ACTTGA>, <IlluminaRunKey: TACGC>)}
        # logging.debug(self.adaptors_full['A08_v4v5_bacteria'][0].illumina_index)

        self.get_user_info()
        self.check_projects()
        if self.errors:
            return
            
        for i in xrange(len(self.csv_content)-1):

            curr_submit_code = self.csv_by_header['submit_code'][i]
            # logging.debug("self.user_info_arr[curr_submit_code] = ")
            # logging.debug(self.user_info_arr[curr_submit_code])

            adaptor    = self.csv_by_header['adaptor'][i]
            dna_region = self.csv_by_header['dna_region'][i]
            domain     = self.csv_by_header['domain'][i]

            self.get_adaptors_full(adaptor, dna_region, domain)

            key = "_".join([adaptor, dna_region, domain])

            # logging.debug(i)
            self.out_metadata[i]['adaptor']				 = self.csv_by_header['adaptor'][i]
            self.out_metadata[i]['amp_operator']		 = self.csv_by_header['op_amp'][i]
            self.out_metadata[i]['barcode']				 = self.csv_by_header['barcode'][i]
            self.out_metadata[i]['barcode_index']		 = self.csv_by_header['barcode_index'][i]
            try:
                if (self.out_metadata[i]['barcode_index'] == ""):
                    self.out_metadata[i]['barcode_index'] = self.adaptors_full[key][0].illumina_index
            except KeyError:
                self.out_metadata[i]['barcode_index'] = ""
            except:
                raise
            # self.out_metadata[i]['contact_name']         = self.user_info_arr[curr_submit_code]['last_name'] + ', ' + self.user_info_arr[curr_submit_code]['first_name']
            # <option value="36">Nicole Webster</option>
            # self.out_metadata[i]['contact_name']         = self.user_info_arr[curr_submit_code]['contact_id']
            self.out_metadata[i]['contact_name']         = self.user_info_arr[curr_submit_code]['first_name'] + ' ' + self.user_info_arr[curr_submit_code]['last_name']
            self.out_metadata[i]['data_owner']           = self.user_info_arr[curr_submit_code]['vamps_name']

            self.out_metadata[i]['dataset']				 = self.csv_by_header['dataset_name'][i]
            self.out_metadata[i]['dataset_description']	 = self.csv_by_header['dataset_description'][i]
            # TODO:
            # $combined_metadata[$num]["dataset_id"]         = get_id($combined_metadata[$num], "dataset", $db_name, $connection);
            # TODO:
            # $combined_metadata[$num]["date_initial"]       = $session["vamps_submissions_arr"][$csv_metadata_row["submit_code"]]["date_initial"];
            # TODO:
            # $combined_metadata[$num]["date_updated"]       = date("Y-m-d");

            self.out_metadata[i]['dna_region']			 = self.csv_by_header['dna_region'][i]
            # TODO:
            # $combined_metadata[$num]["dna_region_id"]      = get_id($session["run_info"], "dna_region_0", $db_name, $connection);

            # TODO: make dropdown menu, camelize, choose
            self.out_metadata[i]['domain']			     = self.csv_by_header['domain'][i]
            self.out_metadata[i]['email']                = self.user_info_arr[curr_submit_code]['email']
            self.out_metadata[i]["env_sample_source_id"] = self.csv_by_header['env_sample_source_id'][i];
            self.out_metadata[i]['env_source_name']      = self.csv_by_header['env_sample_source_id'][i]
            self.out_metadata[i]['first_name']           = self.user_info_arr[curr_submit_code]['first_name']
            self.out_metadata[i]['funding']                = self.vamps_submissions[curr_submit_code]['funding']

            # logging.debug("self.csv_by_header['submit_code'][i] = %s" % self.csv_by_header['submit_code'][i])
            # logging.debug("self.vamps_submissions[curr_submit_code]['institution'] = %s" % self.vamps_submissions[curr_submit_code]['institution'])

            self.out_metadata[i]['insert_size']			 = self.csv_by_header['insert_size'][i]
            self.out_metadata[i]['institution']			 = self.vamps_submissions[curr_submit_code]['institution']
            self.out_metadata[i]['lane']				 = self.csv_by_header['lane'][i]
            self.out_metadata[i]['last_name']            = self.user_info_arr[curr_submit_code]['last_name']
            # TODO:
            # $combined_metadata[$num]["locked"]             = $session["vamps_submissions_arr"][$csv_metadata_row["submit_code"]]["locked"];
            # $combined_metadata[$num]["num_of_tubes"]       = $session["vamps_submissions_arr"][$csv_metadata_row["submit_code"]]["num_of_tubes"];
            # self.out_metadata[i]['nnnn']                 = self.csv_by_header['lane'][i]
            # $combined_metadata[$num]["op_empcr"]           = $csv_metadata_row["op_empcr"];

            self.out_metadata[i]['overlap']				 = self.csv_by_header['overlap'][i]
            self.out_metadata[i]['primer_suite']		 = self.csv_by_header['primer_suite'][i]
            # TODO:
            # $combined_metadata[$num]["primer_suite_id"]    = get_primer_suite_id($combined_metadata[$num]["dna_region"], $combined_metadata[$num]["domain"], $db_name, $connection);

            self.out_metadata[i]['project']				 = self.csv_by_header['project_name'][i]
            
            
            self.out_metadata[i]['project_description']	 = self.vamps_submissions[curr_submit_code]['project_description']
            try:
                self.out_metadata[i]['project_title']		= self.vamps_submissions[curr_submit_code]['title']
            except KeyError:
                try:
                    self.out_metadata[i]['project_title']       = self.vamps_submissions[curr_submit_code]['project_title']
                except KeyError:
                    self.out_metadata[i]['project_title']       = ""
            except:
                raise

            self.out_metadata[i]['read_length']			 = self.csv_by_header['read_length'][i]

            # TODO: get from session["run_info"]["seq_operator"] (run_info upload)
            try:
                self.out_metadata[i]['run_key'] = self.adaptors_full[key][1].illumina_run_key
            except KeyError:
                self.out_metadata[i]['run_key']                = ""
            except:
                raise

            # if (self.csv_by_header['run_key'][i] == ""):
            #     self.out_metadata[i]['run_key'] = self.adaptors_full[key][1].illumina_run_key

            # TODO: get from session["run_info"]["seq_operator"] (run_info upload)
            # self.out_metadata[i]['seq_operator']       = self.csv_by_header['seq_operator'][i]
            self.out_metadata[i]['tubelabel']			 = self.csv_by_header['tube_label'][i]
            """
            for VampsSubmissions and VampsSubmissionsTubes:
            """
            #MIMINUM VampsSubmissionsTubes:
            self.out_metadata[i]['direction']   = self.csv_by_header['direction'][i]
            self.out_metadata[i]['id']          = self.csv_by_header['id'][i]
            self.out_metadata[i]['op_empcr']    = self.csv_by_header['op_empcr'][i]
            self.out_metadata[i]['pool']        = self.csv_by_header['pool'][i]
            self.out_metadata[i]['submit_code'] = self.csv_by_header['submit_code'][i]
            
            # ALL VampsSubmissionsTubes:
            # self.out_metadata[i]['concentration']  = self.csv_by_header['concentration'][i]
            # self.out_metadata[i]['dataset_name']      = self.csv_by_header['dataset_name'][i]
            # self.out_metadata[i]['direction']      = self.csv_by_header['direction'][i]
            # self.out_metadata[i]['duplicate']      = self.csv_by_header['duplicate'][i]
            # self.out_metadata[i]['env_sample_source'] = self.csv_by_header['env_sample_source'][i]
            # self.out_metadata[i]['enzyme']         = self.csv_by_header['enzyme'][i]
            # self.out_metadata[i]['locked']          = self.csv_by_header['locked'][i]
            # self.out_metadata[i]['managed']        = self.csv_by_header['managed'][i]
            # self.out_metadata[i]['num_of_tubes']   = self.csv_by_header['num_of_tubes'][i]
            # self.out_metadata[i]['on_vamps']       = self.csv_by_header['on_vamps'][i]
            # self.out_metadata[i]['op_amp']         = self.csv_by_header['op_amp'][i]
            # self.out_metadata[i]['op_empcr']        = self.csv_by_header['op_empcr'][i]
            # self.out_metadata[i]['op_seq']         = self.csv_by_header['op_seq'][i]
            # self.out_metadata[i]['platform']       = self.csv_by_header['platform'][i]
            # self.out_metadata[i]['pool']            = self.csv_by_header['pool'][i]
            # self.out_metadata[i]['project_name']   = self.csv_by_header['project_name'][i]
            # self.out_metadata[i]['quant_method']    = self.csv_by_header['quant_method'][i]
            # self.out_metadata[i]['rundate']        = self.csv_by_header['rundate'][i]
            # self.out_metadata[i]['runkey']          = self.csv_by_header['runkey'][i]
            # self.out_metadata[i]['sample_received'] = self.csv_by_header['sample_received'][i]
            # self.out_metadata[i]['submit_code']    = self.csv_by_header['submit_code'][i]
            # self.out_metadata[i]['temp_project']   = self.csv_by_header['temp_project'][i]
            # self.out_metadata[i]['title']          = self.csv_by_header['title'][i]
            # self.out_metadata[i]['trim_distal']    = self.csv_by_header['trim_distal'][i]
            # self.out_metadata[i]['tube_label']     = self.csv_by_header['tube_label'][i]
            # self.out_metadata[i]['tube_number']    = self.csv_by_header['tube_number'][i]


        # logging.debug("self.out_metadata = %s" % self.out_metadata)

    def make_metadata_table(self):
        logging.info("make_metadata_table")
        
        self.out_metadata_table['headers'] = self.HEADERS_TO_EDIT_METADATA

        for i in xrange(len(self.out_metadata.keys())):
            self.out_metadata_table['rows'].append({})

        # logging.debug("OOO self.out_metadata_table = %s" % self.out_metadata_table)

        for r_num, v in self.out_metadata.items():
            for header in self.HEADERS_TO_EDIT_METADATA:
                try:
                    self.out_metadata_table['rows'][int(r_num)][header] = (self.out_metadata[r_num][header])
                except KeyError as e:
                    logging.warning("KeyError, e = %s" % e)
                    self.out_metadata_table['rows'][int(r_num)][header] = ""
                except:
                    raise

        # logging.debug("self.out_metadata_table BBB = %s" % self.out_metadata_table)

    def insert_project(self, request_post):
        project_name = request_post['project_0'] + "_" + request_post['project_1'] + "_" + request_post['project_2'] + request_post['project_3']

        owner = Contact.cache_all_method.get(contact = request_post['contact'])

        # logging.debug("NNN project_name = %s, project_title = %s, funding = %s, env_sample_source_id = %s, contact_id = %d" % (project_name, request_post['project_title'], request_post['funding'], request_post['env_source_name'], owner.contact_id))

        return Project.objects.get_or_create(project=project_name, title=request_post['project_title'], project_description=request_post['project_description'], rev_project_name=project_name[::-1], funding=request_post['funding'], env_sample_source_id=request_post['env_source_name'], contact_id=owner.contact_id)

        # return created

    def csv_file_upload(self, request):

        csv_file = request.FILES['csv_file']
        if csv_file.size == 0:
            self.errors.append("The file %s is empty or does not exist." % csv_file)
            return ("", 'no_file')

            # render(request, 'submission/upload_metadata.html', {'errors': self.errors, 'errors_size': len(self.errors) })

        has_empty_cells = self.import_from_file(csv_file)

        if has_empty_cells:                
            self.errors.append("The following csv fields should not be empty: %s" % ", ".join(self.empty_cells))
            return ("", 'has_empty_cells')

        # TODO:
        # validate size and type of the file
        # tmp_path = 'tmp/%s' % csv_file
        # default_storage.save(tmp_path, ContentFile(csv_file.file.read()))
        # full_tmp_path = os.path.join(settings.BASE_DIR, tmp_path)
        # - See more at: http://blog.hayleyanderson.us/2015/07/18/validating-file-types-in-django/#sthash.Ux4hWNaD.dpuf
        # csv_validation = Validation()
        # csv_validation.required_cell_values_validation()

        self.get_initial_run_info_data_dict()
        self.get_selected_variables(request.POST)
        request.session['run_info_from_csv'] = self.run_info_from_csv
        metadata_run_info_form = CsvRunInfoUploadForm(initial=request.session['run_info_from_csv'])

        # # TODO: move to one method in metadata_tools, call from here as create info and create csv
        # request.session['lanes_domains'] = self.get_lanes_domains()
        # del request.session['lanes_domains']

        self.get_vamps_submission_info()

        self.get_csv_by_header()

        self.get_adaptor_from_csv_content()

        self.make_new_out_metadata()
        if self.errors:
            return (metadata_run_info_form, has_empty_cells)
            
        request.session['out_metadata'] = self.out_metadata

        # 

        # utils.is_local(request)
        # HOSTNAME = request.get_host()
        # if HOSTNAME.startswith("localhost"):
        #     logging.debug("local")

        return (metadata_run_info_form, has_empty_cells)

    def submit_new_project(self, request):
        # logging.debug("EEE: request.POST = %s" % request.POST)

        # request.session['run_info_from_csv'] = self.run_info_from_csv
        # logging.debug("request.session['run_info_from_csv'] 111 = ")
        # logging.debug(request.session['run_info_from_csv'])

        # try:
        #     metadata_run_info_form = CsvRunInfoUploadForm(initial=request.session['run_info_from_csv'])
        # except KeyError as e:
        #     metadata_run_info_form = CsvRunInfoUploadForm()
        #     logging.debug("request.session['run_info_from_csv'] does not exist")
        # except:
        #     raise


        metadata_new_project_form = AddProjectForm(request.POST)

        if metadata_new_project_form.is_valid():        
            # logging.debug("!!!metadata_new_project_form.cleaned_data")
            # logging.debug(metadata_new_project_form.cleaned_data)
            """
            !!!metadata_new_project_form.cleaned_data
            {'env_source_name': <EnvSampleSource: 0: >, 'project_description': u'www', 'funding': u'rrr', 'project_title': u'sss', 'project': u'dfsdfs_dsfsdfs_B_v6', 'contact': <Contact: Eric Boyd>}

            """

            self.new_project, self.new_project_created = self.insert_project(request.POST)

        return metadata_new_project_form

    def submit_run_info(self, request):
        self.get_selected_variables(request.POST)
        request.session['run_info'] = {}
        request.session['run_info']['selected_rundate']         = self.selected_rundate
        request.session['run_info']['selected_machine_short']   = self.selected_machine_short
        request.session['run_info']['selected_machine']         = self.selected_machine
        request.session['run_info']['selected_dna_region']      = self.selected_dna_region
        request.session['run_info']['selected_overlap']         = self.selected_overlap

        # logging.debug("RRR request.POST from submit_run_info")
        # logging.debug(request.POST)

            # self.out_metadata[i]['nnnn']                 = self.csv_by_header['lane'][i]

        #*) metadata table to show and edit
        self.edit_out_metadata(request)
        request.session['out_metadata'] = self.out_metadata

        self.make_metadata_table()

        # metadata_run_info_form = CsvRunInfoUploadForm(initial=request.session['run_info_from_csv'])
        metadata_run_info_form = CsvRunInfoUploadForm(request.POST)
        request.session['run_info_form_post'] = request.POST

        MetadataOutCsvFormSet = formset_factory(MetadataOutCsvForm, max_num = len(self.out_metadata_table['rows']))
        formset = MetadataOutCsvFormSet(initial=self.out_metadata_table['rows'])

        request.session['out_metadata_table'] = self.out_metadata_table

        return (request, metadata_run_info_form, formset)

    def create_submission_metadata_file(self, request):
        # logging.debug("EEE: request.POST = %s" % request.POST)

        """
        *) metadata table to show and edit
        *) metadata out edit
        *) ini and csv machine_info/run dir
        *) ini files
        *) metadata csv files
        """

        #*) metadata table to show and edit
        self.edit_out_metadata_table(request)
        metadata_run_info_form = CsvRunInfoUploadForm(request.session['run_info_form_post'])

        MetadataOutCsvFormSet = formset_factory(MetadataOutCsvForm)

        my_post_dict = self.edit_post_metadata_table(request)

        self.add_out_metadata_table_to_out_metadata(request)

        #*) metadata out edit
        self.out_metadata = request.session['out_metadata']
        self.update_out_metadata(my_post_dict, request)

        # adaptor    = self.csv_by_header['adaptor'][i]
        # dna_region = self.csv_by_header['dna_region'][i]
        # domain     = self.csv_by_header['domain'][i]
        #
        # self.get_adaptors_full(adaptor, dna_region, domain)

        # ----
        self.selected_rundate       = request.session['run_info']['selected_rundate']
        self.selected_machine_short = request.session['run_info']['selected_machine_short']
        self.selected_machine       = request.session['run_info']['selected_machine']
        self.selected_dna_region    = request.session['run_info']['selected_dna_region']
        self.selected_overlap       = request.session['run_info']['selected_overlap']

        #*) ini and csv machine_info/run dir
        self.lanes_domains = self.utils.get_lanes_domains(self.out_metadata)
        self.create_path_to_csv()

        # *) validation
        formset = MetadataOutCsvFormSet(my_post_dict)

        if len(metadata_run_info_form.errors) == 0 and formset.total_error_count() == 0:

            #*) ini files
            self.create_ini_names()
            self.write_ini()

            #*) metadata csv files
            self.make_out_metadata_csv_file_names()
            self.write_out_metadata_to_csv(my_post_dict, request)

            # *) check if csv was created
            self.check_out_csv_files()
            
            self.update_submission_tubes(request)
            
        self.new_rundate, self.new_rundate_created = self.insert_run(request)
        logging.info("self.new_rundate = %s, self.new_rundate_created = %s" % (self.new_rundate, self.new_rundate_created))
        
        return (request, metadata_run_info_form, formset)
        
    def insert_run(self, request):
        return Run.objects.get_or_create(run=request.session['run_info']['selected_rundate'], run_prefix='illumin', platform=request.session['run_info']['selected_machine'])
    
    def update_submission_tubes(self, request):
        try:
            self.out_metadata = request.session['out_metadata']
            # logging.debug("self.out_metadata = ")
            # logging.debug(self.out_metadata)
        except:
            raise
        
        overlap_choices = dict(Overlap.OVERLAP_CHOICES)
        
        for i in self.out_metadata.keys():
            barcode = self.out_metadata[i]['barcode']
            direction = self.out_metadata[i]['direction']
            env_sample_source_id = self.out_metadata[i]['env_sample_source_id']
            id = self.out_metadata[i]['id']
            insert_size = int(self.out_metadata[i]['insert_size'])
            lane = self.out_metadata[i]['lane']
            op_amp = self.out_metadata[i]['amp_operator']
            op_empcr = self.out_metadata[i]['op_empcr']
            op_seq = request.session['run_info_form_post']['csv_seq_operator']
            overlap = overlap_choices[self.out_metadata[i]['overlap']]
            platform = request.session['run_info']['selected_machine']
            pool = self.out_metadata[i]['pool']
            project_name = self.out_metadata[i]['project']
            read_length = self.out_metadata[i]['read_length']
            rundate = request.session['run_info']['selected_rundate']
            submit_code = self.out_metadata[i]['submit_code']
            
            updated =  models_l_vamps.VampsSubmissionsTubes.objects.filter(id = id, submit_code = submit_code).update(
                barcode = barcode,
                direction = direction,
                insert_size = insert_size,
                lane = lane,
                op_amp = op_amp,
                op_empcr = op_empcr,
                op_seq = op_seq,
                overlap = overlap,
                platform = platform,
                pool = pool,
                project_name = project_name,
                read_length = read_length,
                rundate = rundate,
                date_updated = datetime.now()
            )
            """
            empty on vamps:
            barcode
            direction
            enzyme
            lane
            on_vamps
            op_amp
            op_empcr
            op_seq
            platform
            pool
            rundate
            sample_received

            
            """
            logging.info("VampsSubmissionsTubes updated = %s" % (updated))
            
            # print "UUU updated = "
            # print updated


