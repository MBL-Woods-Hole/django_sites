from datetime import datetime
from .models import *
import csv
import codecs
import time
from .utils import Utils

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection, transaction  

from collections import defaultdict

class CsvMetadata():

    def __init__(self):

        self.RUN_INFO_FORM_FIELD_HEADERS = ["dna_region", "insert_size", "op_seq", "overlap", "read_length", "rundate"]
        self.csv_headers = []
        self.csv_content = []
        self.run_info_from_csv = {}
        self.errors = []
        self.csv_by_header_uniqued = defaultdict( list )
        self.csvfile = ""

        # error = True

        self.HEADERS = {'id': {'field':'id', 'required':True},
                        'submit_code': {'field':'submit_code', 'required':True},
                        'user': {'field':'user', 'required':True},
                        'tube_number': {'field':'tube_number', 'required':True},
                        'tube_label': {'field':'tube_label', 'required':True},
                        'dataset_description': {'field':'dataset_description', 'required':True},
                        'duplicate': {'field':'duplicate', 'required':True},
                        'domain': {'field':'domain', 'required':True},
                        'primer_suite': {'field':'primer_suite', 'required':True},
                        'dna_region': {'field':'dna_region', 'required':True},
                        'project_name': {'field':'project_name', 'required':True},
                        'dataset_name': {'field':'dataset_name', 'required':True},
                        'runkey': {'field':'runkey', 'required':True},
                        'barcode': {'field':'barcode', 'required':True},
                        'pool': {'field':'pool', 'required':True},
                        'lane': {'field':'lane', 'required':True},
                        'direction': {'field':'direction', 'required':True},
                        'platform': {'field':'platform', 'required':True},
                        'op_amp': {'field':'op_amp', 'required':True},
                        'op_seq': {'field':'op_seq', 'required':True},
                        'op_empcr': {'field':'op_empcr', 'required':True},
                        'enzyme': {'field':'enzyme', 'required':True},
                        'rundate': {'field':'rundate', 'required':True},
                        'adaptor': {'field':'adaptor', 'required':True},
                        'date_initial': {'field':'date_initial', 'required':True},
                        'date_updated': {'field':'date_updated', 'required':True},
                        'on_vamps': {'field':'on_vamps', 'required':True},
                        'sample_received': {'field':'sample_received', 'required':True},
                        'concentration': {'field':'concentration', 'required':True},
                        'quant_method': {'field':'quant_method', 'required':True},
                        'overlap': {'field':'overlap', 'required':True},
                        'insert_size': {'field':'insert_size', 'required':True},
                        'barcode_index': {'field':'barcode_index', 'required':True},
                        'read_length': {'field':'read_length', 'required':True},
                        'trim_distal': {'field':'trim_distal', 'required':True},
                        'env_sample_source_id': {'field':'env_sample_source_id', 'required':True},}

        self.required_headers = [header_name for header_name, values in
                                 self.HEADERS.items() if values['required']]


    def import_from_file(self, csvfile):
        self.csvfile = csvfile
        dialect = self.get_dialect()
        reader = self.get_reader(dialect)

        self.csv_headers, self.csv_content = self.parce_csv(reader)

        self.check_headers_presence(reader)

        self.get_csv_by_header_uniqued()


        # writer = csv.DictWriter(doc,
        #                         ["dna_region", "rundate"])
        #
        # for row in self.csv_content:
        #     writer.writerow({'dna_region': row.dna_region, 'rundate': row.rundate})
        #     print writer

    def get_dialect(self):
        try:
            dialect = csv.Sniffer().sniff(codecs.EncodedFile(self.csvfile, "utf-8").read(1024))
            return dialect
        except csv.Error as e:
            self.errors.append('%s is not a valid CSV file' % (self.csvfile))
        except:
            raise

    def get_reader(self, dialect):
        try:
            self.csvfile.open()
            return csv.reader(codecs.EncodedFile(self.csvfile, "utf-8"), delimiter=',', dialect=dialect)
        except csv.Error as e:
            self.errors.append('%s is not a valid CSV file' % (self.csvfile))
        except:
            raise

    def get_csv_by_header(self): # not using it
        self.csv_by_header = defaultdict( list )

        for row in zip(*self.csv_content):
            self.csv_by_header[row[0]] = row[1:]

    def get_csv_by_header_uniqued(self):
        self.csv_by_header_uniqued = dict((x[0], list(set(x[1:]))) for x in zip(*self.csv_content))
        print "self.csv_by_header_uniqued: "
        print self.csv_by_header_uniqued

    def get_initial_run_info_data_dict(self):
        try:
            csv_rundate = "".join(self.csv_by_header_uniqued['rundate'])

            self.run_info_from_csv = {'csv_rundate': csv_rundate,
            'csv_path_to_raw_data': "/xraid2-2/sequencing/Illumina/%s" % csv_rundate,
            'csv_dna_region':	    "".join(self.csv_by_header_uniqued['dna_region']),
            'csv_overlap':		    "".join(self.csv_by_header_uniqued['overlap']),
            'csv_has_ns':		    "".join(self.csv_by_header_uniqued['rundate']),
            'csv_seq_operator':	    "".join(self.csv_by_header_uniqued['op_seq']),
            'csv_insert_size':	    "".join(self.csv_by_header_uniqued['insert_size']),
            'csv_read_length':	    "".join(self.csv_by_header_uniqued['read_length'])}
        except KeyError as e:
            cause = e.args[0]
            self.errors.append('There is no data for %s in the file %s' % (cause, self.csvfile))
        except:
            raise

    def parce_csv(self, reader):
      for y_index, row in enumerate(reader):
          self.csv_content.append(row)
          if y_index == 0:
              self.csv_headers = [header_name.lower() for header_name in row if header_name]
              continue
      return self.csv_headers, self.csv_content

    def check_headers_presence(self, reader):
      missing_headers = set(self.required_headers) - set([r.lower() for r in self.csv_headers])
      if missing_headers:
          missing_headers_str = ', '.join(missing_headers)
          self.errors.append('Missing headers: %s' % (missing_headers_str))
          # print "self.errors 3"
          # print self.errors
          # raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
          return False
      return True

    def required_cell_values_validation(self, reader):
      # sanity check required cell values
      for y_index, row in enumerate(reader):
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
        for submit_code in self.csv_by_header_uniqued['submit_code']:            
            query_subm = """SELECT subm.*, auth.user, auth.passwd, auth.first_name, auth.last_name, auth.active, auth.security_level, auth.email, auth.institution, auth.date_added 
                FROM %s.vamps_submissions AS subm
                JOIN %s.vamps_auth AS auth
                  ON (auth.id = subm.vamps_auth_id)
                WHERE submit_code = \"%s\"""" % (db_name, db_name, submit_code)
            self.create_csv(query_subm, out_file_name)
    
