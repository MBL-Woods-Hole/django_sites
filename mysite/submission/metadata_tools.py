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
        self.csv_by_header = defaultdict( list )
        self.csvfile = ""
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
        return 'There is no data for <span class="emph_it">%s</span> in the file <span class="emph_it">%s</span>' % (self.cause, self.csvfile)

    def import_from_file(self, csvfile):
        print "csvfile"
        print csvfile
        self.csvfile = csvfile
        dialect = self.get_dialect()
        print "dialect = "
        print dialect

        self.get_reader(dialect)
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

    def get_dialect(self):
        try:
            # dialect = csv.Sniffer().sniff(self.csvfile.read(1024), delimiters=";,")
            # dialect = csv.Sniffer().sniff(self.csvfile.read(1024), ",")
            # dialect = csv.Sniffer().sniff(self.csvfile.read(1024), delimiters=";,")

            dialect = csv.Sniffer().sniff(codecs.EncodedFile(self.csvfile, "utf-8").read(1024), delimiters=',')
            if dialect:
              self.csvfile.seek(0)
              print "dialect.delimiter"
              print dialect.delimiter
              # print dir(dialect)
              # ['__doc__', '__init__', '__module__', '_name', '_valid', '_validate', 'delimiter', 'doublequote', 'escapechar', 'lineterminator', 'quotechar', 'quoting', 'skipinitialspace']
              
              # print "----"
              return dialect
            else:
              print("WARNING, file %s is empty (size = %s), check it's path" % (self.csvfile.name, self.csvfile.size))

        except csv.Error as e:
            self.errors.append('Warning for %s: %s' % (self.csvfile, e))
        except:
            raise

    def get_reader(self, dialect):
        try:
            self.csvfile.open()
            self.reader = csv.reader(codecs.EncodedFile(self.csvfile, "utf-8"), delimiter=',', dialect=dialect)
        except csv.Error as e:
            self.errors.append('%s is not a valid CSV file: %s' % (self.csvfile, e))
        except:
            raise

    def get_csv_by_header(self): # not using it
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
        print "IIIIN HERE, out_file_name = %s, self.path_to_csv = %s" % (out_file_name, self.path_to_csv)

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


    def make_metadata_table(self):
        num = 0
        out_metadata = defaultdict( lambda: defaultdict(int) )
        print "self.HEADERS_TO_CSV = %s" % self.HEADERS_TO_CSV
        # 'adaptor', 'amp_operator', 'barcode', 'barcode_index', 'data_owner', 'dataset', 'dataset_description', 'dna_region', 'email', 'env_sample_source_id', 'first_name', 'funding', 'insert_size', 'institution', 'lane', 'last_name', 'overlap', 'primer_suite', 'project', 'project_description', 'project_title', 'read_length', 'run', 'run_key', 'seq_operator', 'tubelabel'
        # out_metadata.append(self.HEADERS_TO_CSV)
        self.get_csv_by_header()
        for k, v in self.csv_by_header.items():
            print "for k, v in self.csv_by_header: k = %s, v = %s" % (k, v)
        print "=" * 8 
        print "self.csv_content:"
        print self.csv_content
        print "=" * 8 
        print "len(self.csv_content)"
        print len(self.csv_content)
        
        
        for header in self.HEADERS_TO_CSV:
            for idx, item in enumerate(self.csv_by_header[header]):
                print "idx = %s, header = %s, item = %s" % (idx, header, item)
                # print "idx = %s, col = %s, cell = %s" % (idx, header, self.csv_by_header[header])
                try:
                    out_metadata[idx][header] = self.csv_by_header[header][idx]
                except IndexError:
                    out_metadata[idx][header] = ""
                except:
                    raise

        print "OOO out_metadata"
        print out_metadata
        print "OOO out_metadata  end"
        
        # for k1, v1 in out_metadata.items():
        #     print "\n=======\nfor k1, v1 in out_metadata: k1 = %s, v1 = %s" % (k1, v1)

            
        #   print "cell.count = %s" % (len(self.csv_by_header[h]))
          # if (cell.count > 0):
          #     for
          # cell.count = 2
          # col = primer_suite, cell = ('Archaeal V6 Suite', 'Bacterial V6 Suite')
          # cell.count = 0
          # col = run_key, cell = []
          
          # cell.dir = ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
#
        num += 1

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
