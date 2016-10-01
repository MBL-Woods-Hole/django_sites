import sys
import models
from .utils import Utils, Dirs

from datetime import datetime

import csv
import codecs
import time
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection, transaction

from collections import defaultdict

# Assuming that in each csv one rundate and one platform!
class CsvMetadata():

    def __init__(self):

        self.RUN_INFO_FORM_FIELD_HEADERS = ["dna_region", "insert_size", "op_seq", "overlap", "read_length", "rundate"]
        self.csv_headers = []
        self.csv_content = []
        self.run_info_from_csv = {}
        self.errors = []
        self.csv_by_header_uniqued = defaultdict( list )
        # self.csv_file_name = "submission/selenium_tests/ashipunova354276_VAMPS_submission_good.csv"
        self.csv_file = ""
        self.cause = ""
        self.path_to_csv = ""
        self.selected_lane = ""
        self.domain_letter = ""
        self.selected_machine_short = ""
        self.ini_names = {}
        self.dirs = Dirs()
        self.lanes_domains = []

        # error = True

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
            'runkey': {'field': 'runkey', 'required': True},
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
        
        self.HEADERS_TO_CSV = ['adaptor', 'amp_operator', 'barcode', 'barcode_index', 'data_owner', 'dataset', 'dataset_description', 'dna_region', 'email', 'env_sample_source_id', 'first_name', 'funding', 'insert_size', 'institution', 'lane', 'last_name', 'overlap', 'primer_suite', 'project', 'project_description', 'project_title', 'read_length', 'run', 'run_key', 'seq_operator', 'tubelabel']

        self.required_headers = [header_name for header_name, values in
                                 self.HEADERS_FROM_CSV.items() if values['required']]
        print "self.required_headers = %s" % self.required_headers

    def no_data_message(self):
        return 'There is no data for <span class="emph_it">%s</span> in the file <span class="emph_it">%s</span>' % (self.cause, self.csv_file)

    def upload(self, request):
      input_file = request.FILES.get('csv_file')
      input_file.seek(0)
      
      print "=== DDD1 ==="
      print type(input_file)
      input_file.seek(0)
      
      print "input_file.field_name"
      print input_file.field_name
      input_file.seek(0)
      
# csv_file
      print "=== input_file.file"
      print input_file.file
      input_file.seek(0)
      
# <_io.BytesIO object at 0x110d34050>

      print "=== input_file.name"
      print input_file.name
      input_file.seek(0)
      
# ashipunova354276_VAMPS_submission_good.csv
#       print "=== input_file.newlines"
#       print input_file.newlines
# AttributeError: '_io.BytesIO' object has no attribute 'newlines'

      print "=== input_file.read"
      input_file.seek(0)
      print input_file.read
      input_file.seek(0)
      
# <built-in method read of _io.BytesIO object at 0x10b0f2050>

      print "=== input_file.readline"
      input_file.seek(0)
      print input_file.readline
      input_file.seek(0)
      
# <built-in method readline of _io.BytesIO object at 0x10b0f2050>

      print "=== input_file.size"
      input_file.seek(0)
      print input_file.size
      input_file.seek(0)
      
# 0
      print "=== input_file.seek"
      print input_file.seek
      input_file.seek(0)
      
      # <built-in method seek of _io.BytesIO object at 0x10b0f2050>
      
      print "=== input_file.tell"
      print input_file.tell
      input_file.seek(0)
      
      # <built-in method tell of _io.BytesIO object at 0x10b0f2050>
      

      print "=== DDD1 end ==="
      # print django.core.files.uploadedfile.InMemoryUploadedFile.__dir__
      print "dir(input_file)"
      print dir(input_file)
      # print "help(input_file)"
      # print help(input_file)
      # print "help(uploadedfile)"
      # print help(uploadedfile)
      # try:
      #     rr = input_file.readlines()
      #     print "rr"
      #     print rr
          
          # wb = xlrd.open_workbook(tmp)
          # ...  # do what you have to do
      # finally:
      #     os.unlink(tmp)  # delete the temp file no matter what
      # except:
      #   raise
        
      print "=== DDD0 paramFile ==="
      print request.FILES['csv_file'].read()
      # print type(paramFile)
      # print "paramFile"
      # print paramFile
      # portfolio = csv.DictReader(paramFile)
      # print "=== DDD1 ==="
      # print type(portfolio)
      # users = []
      # for row in portfolio:
      #   print "=== DDD2 ==="
      #   print row
      #   print "==="
      #   users.append(row)
      #
      # for row1 in users:
      #   print "=== DDD3 ==="
      #   print row1
      #   print "==="    


        # # data = csv.DictReader(request.FILES['file'])
        #
        # # paramFile = request.FILES['file'].read()
        # # data = csv.DictReader(paramFile)
        # data = csv.reader(request.FILES['csv_file'].)
        #
        # list1 = []
        # for row in data:
        #     print "RRR row"
        #     print row
        #     list1.append(row)
        # print "=== DDD ==="
        # # print data
        # print list1
        # print "==="
        

    def import_from_file(self, csv_file):
        print "csv_file"
        print csv_file
        print "csv_file.name"
        print csv_file.name
        self.csv_file = csv_file
        

        # lines = ["'A','bunch+of','multiline','CSV,LIKE,STRING'"]
        # 
        # reader = csv.reader(lines, quotechar="'")
        # 
        # with open('out.csv', 'wb') as f:
        #    writer = csv.writer(f)
        #    writer.writerows(list(reader))
        # 
        
        # try:
        #   dialect = csv.get_dialect(self.csv_file)
        #   print "dialect = "
        #   print dialect
        #   if (dialect)
        # csv_file_name = "submission/selenium_tests/ashipunova354276_VAMPS_submission_good.csv"
        # TODO: get path from where?
        csvfile_o = open(os.path.join("submission/selenium_tests", csv_file.name), 'rb')
        # csvfile_o = open(csv_file_name, 'rb')
        dialect = csv.Sniffer().sniff(csvfile_o.read(1024))
        csvfile_o.seek(0)
        self.reader = csv.reader(csvfile_o, dialect)


        # self.get_reader(dialect)
        # self.get_reader()
        print "LLL self.reader"
        print self.reader

        self.csv_headers, self.csv_content = self.parce_csv()

        self.check_headers_presence()

        self.get_csv_by_header_uniqued()


        # writer = csv.DictWriter(doc,
        #                         ["dna_region", "rundate"])
        #
        # for row in self.csv_content:
        #     writer.writerow({'dna_region': row.dna_region, 'rundate': row.rundate})
        #     print writer

    # def get_dialect(self):
    #     try:
    #         # dialect = csv.Sniffer().sniff(self.csv_file.read(1024), delimiters=";,")
    #         # dialect = csv.Sniffer().sniff(self.csv_file.read(1024), ",")
    #         # dialect = csv.Sniffer().sniff(self.csv_file.read(1024), delimiters=";,")
    #         try:
    #             # with open(r'ashipunova354276_VAMPS_submission_good.csv', 'rb') as csv_file:
    #             with open(self.csv_file_name, 'rb') as o_csv_file:
    #                 reader = csv.reader(o_csv_file, delimiter=',') 
    #                 for row in reader:
    #                     print (', '.join(row))
    #         except IOError:
    #             print ("IOError: " + self.csv_file_name)
    #             sys.exit()

            # dialect = csv.Sniffer().sniff(codecs.EncodedFile(self.csv_file, "utf-8").read(1024), delimiters=',')
            # self.csv_file.seek(0)
            # print "dialect.delimiter"
            # print dialect.delimiter
            # return dialect
        # except csv.Error as e:
        #     self.errors.append('Warning for %s: %s' % (self.csv_file, e))
        # except:
        #     raise

    # def get_reader(self, dialect):
    def get_reader(self):
        try:
            self.csv_file.open()
            # self.reader = csv.reader(codecs.EncodedFile(self.csv_file, "utf-8"), delimiter=',', dialect=dialect)
            self.reader = csv.reader(codecs.EncodedFile(self.csv_file, "utf-8"), delimiter=',')
            
        except csv.Error as e:
            self.errors.append('%s is not a valid CSV file: %s' % (self.csv_file, e))
        except:
            raise

    def get_csv_by_header(self): # not using it
        self.csv_by_header = defaultdict( list )

        for row in zip(*self.csv_content):
            self.csv_by_header[row[0]] = row[1:]

    def get_csv_by_header_uniqued(self):
        self.csv_by_header_uniqued = ""
        self.csv_by_header_uniqued = dict((x[0], list(set(x[1:]))) for x in zip(*self.csv_content))
        print "self.csv_by_header_uniqued: "
        print self.csv_by_header_uniqued

    def get_initial_run_info_data_dict(self):
        try:
            csv_rundate = "".join(self.csv_by_header_uniqued['rundate'])

            self.run_info_from_csv = {
                'csv_rundate':          csv_rundate,
                'csv_path_to_raw_data': "/xraid2-2/sequencing/Illumina/%s%s" % (csv_rundate, self.selected_machine_short),
                'csv_platform':	        "".join(self.csv_by_header_uniqued['platform']),
                'csv_dna_region':	    "".join(self.csv_by_header_uniqued['dna_region']),
                'csv_overlap':		    "".join(self.csv_by_header_uniqued['overlap']),
                'csv_has_ns':		    "".join(self.csv_by_header_uniqued['rundate']),
                'csv_seq_operator':	    "".join(self.csv_by_header_uniqued['op_seq']),
                'csv_insert_size':	    "".join(self.csv_by_header_uniqued['insert_size']),
                'csv_read_length':	    "".join(self.csv_by_header_uniqued['read_length'])
            }

            print "RRR self.run_info_from_csv"
            print self.run_info_from_csv
        except KeyError as e:
            self.cause = e.args[0]
            self.errors.append(self.no_data_message())
        except:
            raise

    def parce_csv(self):
      for y_index, row in enumerate(self.reader):
          print "parce_csv row"
          print row

          self.csv_content.append(row)
          if y_index == 0:
              self.csv_headers = [header_name.lower() for header_name in row if header_name]
              continue
      return self.csv_headers, self.csv_content

    def check_headers_presence(self):
      missing_headers = set(self.required_headers) - set([r.lower() for r in self.csv_headers])
      if missing_headers:
          missing_headers_str = ', '.join(missing_headers)
          self.errors.append('Missing headers: %s' % (missing_headers_str))
          # print "self.errors 3"
          # print self.errors
          # raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
          return False
      return True

    def create_csv(self, query, out_file_name):
        cursor = connection.cursor()
        cursor.execute(query)
        csv_writer = csv.writer(open(out_file_name, "wb"), delimiter=',')
        csv_writer.writerow([i[0] for i in cursor.description]) # write headers
        csv_writer.writerows(cursor)
        del csv_writer # this will close the CSV file

    def get_vamps_submission_info(self):
        db_name = "test_vamps"
        out_file_name = "temp_subm_info"
        try:
            for submit_code in self.csv_by_header_uniqued['submit_code']:
                query_subm = """SELECT subm.*, auth.user, auth.passwd, auth.first_name, auth.last_name, auth.active, auth.security_level, auth.email, auth.institution, auth.date_added
                    FROM %s.vamps_submissions AS subm
                    JOIN %s.vamps_auth AS auth
                      ON (auth.id = subm.vamps_auth_id)
                    WHERE submit_code = \"%s\"""" % (db_name, db_name, submit_code)
                self.create_csv(query_subm, out_file_name)
        except KeyError as e:
            self.cause = e.args[0]
            self.errors.append(self.no_data_message())
        except:
            raise

    def get_selected_variables(self):
        print "self.csv_by_header_uniqued['platform']"
        print self.csv_by_header_uniqued['platform']
        self.selected_machine = "".join(self.csv_by_header_uniqued['platform']).lower()
        print "self.selected_machine"
        print self.selected_machine
        self.selected_rundate = "".join(self.csv_by_header_uniqued['rundate']).lower()
        machine_shortcuts_choices = dict(models.Machine.MACHINE_SHORTCUTS_CHOICES)
        print "MMM machine_shortcuts_choices"
        print machine_shortcuts_choices
        self.selected_machine_short = machine_shortcuts_choices[self.selected_machine]

    def create_path_to_csv(self):
        #/xraid2-2/g454/run_new_pipeline/illumina/miseq_info/20160711
        self.path_to_csv = os.path.join(settings.ILLUMINA_RES_DIR, self.selected_machine + "_info", self.selected_rundate)
        print "self.path_to_csv"
        print self.path_to_csv
        new_dir = self.dirs.check_and_make_dir(self.path_to_csv)

    def create_ini_names(self):
        # 20160711_ms_1_B_run_info.ini
        # 20150101_hs_hiseq_A_run_info.ini
        # 20150101_hs_hiseq_B_run_info.ini
        for lane_domain in self.lanes_domains:
            print "for lane_domain in self.lanes_domains lane_domain = %s" % lane_domain
            self.ini_names[lane_domain] = "%s_%s_%s_run_info.ini" % (self.selected_rundate, self.selected_machine_short, lane_domain)

        print "self.ini_names"
        print self.ini_names

    def get_lanes_domains(self):
        domain_choices = dict(models.Domain.LETTER_BY_DOMAIN_CHOICES)

        for domain_name in self.csv_by_header_uniqued['domain']:
            domain_letter = domain_choices[domain_name]
            for lane in self.csv_by_header_uniqued['lane']:
                self.lanes_domains.append("%s_%s" % (lane, domain_letter))

    def write_ini(self):
        for lane_domain, ini_name in self.ini_names.items():    
            ini_text = '''{"rundate":"%s","lane_domain":"%s","dna_region":"%s","path_to_raw_data":"%s","overlap":"%s"}
            ''' % (self.run_info_from_csv['csv_rundate'], lane_domain, self.run_info_from_csv['csv_dna_region'], self.run_info_from_csv['csv_path_to_raw_data'], self.run_info_from_csv['csv_overlap']) 

            ini_file = open(os.path.join(self.path_to_csv, ini_name), 'w')
            ini_file.write(ini_text)
            ini_file.close()

class Validation(CsvMetadata):
    def __init__(self):
        CsvMetadata.__init__(self)
        # print "AAA"
        # print self.HEADERS_FROM_CSV
        print "CCC1 required_cell_values_validation"
        print self.reader

    def required_cell_values_validation(self):
        print "CCC required_cell_values_validation"
        print self.reader

        # sanity check required cell values
        for y_index, row in enumerate(self.reader):
            print "YYY y_index"
            print y_index
            print "WWW row"
            print row
            # ignore blank rows
            # if not ''.join(str(x) for x in row):
            #     continue

            for x_index, cell_value in enumerate(row):
                # if indexerror, probably an empty cell past the headers col count
                try:
                    self.csv_headers[x_index]
                except IndexError:
                    continue
                if self.csv_headers[x_index] in self.required_headers:
                    if not cell_value:
                        self.errors.append('Missing required value %s for row %s' %
                                                (self.csv_headers[x_index], y_index + 1))
                        # print "self.errors 4"
                        # print self.errors


                        # raise ValidationError(u'Missing required value %s for row %s' %
                                                # (self.csv_headers[x_index], y_index + 1))