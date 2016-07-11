from datetime import datetime
from .models import *
import csv

from django.conf import settings
from django.core.exceptions import ValidationError

from collections import defaultdict

class CodeCSvModel():
  
    def __init__(self):
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

        self.RUN_INFO_FORM_FIELD_HEADERS = ["dna_region", "insert_size", "op_seq", "overlap", "read_length", "rundate"]

        # codeid = models.SmallIntegerField(primary_key=True)
        # remotecode = models.CharField(max_length=32)
        # active = models.BooleanField()
        # created = models.DateField()
        # modified = models.DateField()
        # incentiveid = models.CharField(max_length=32)
        #     
        self.csv_headers = []
        self.csv_content = []

    # class Meta:
        # delimiter = ";"
        # dbModel = Code

    def import_from_file(self, file_name):
        print "file_name from CodeCSvModel.import_from_file"
        print file_name
        try:
            doc = file_name['csv']
            dialect = csv.Sniffer().sniff(doc.read(1024))
            doc.seek(0, 0)
            print "dialect = "
            print dialect
        except csv.Error:
            raise ValidationError(u'Not a valid CSV file')
    
        reader = csv.reader(doc.read().splitlines(), dialect)
        print "reader = "
        print reader
        self.csv_headers = []
        required_headers = [header_name for header_name, values in
                            self.HEADERS.items() if values['required']]
        print "required_headers = "
        print required_headers
    
        # for index, row in enumerate(reader):
        #   print "III index, row"
        #   print index, row
    
        self.csv_headers, self.csv_content = self.parce_csv(reader)

        print "self.csv_headers"
        print self.csv_headers

        print "self.csv_content"
        print self.csv_content
        
        # self.csv_by_header = zip(*self.csv_content)

        self.csv_by_header = defaultdict( list )
        aa = defaultdict( list )
        
        # for tuple in a:
        for x, y, z in zip(*self.csv_content):
            self.csv_by_header[x] = (y,z)
            
        aa = {key: (value1, value2) for (key, value1, value2) in zip(*self.csv_content) }
        
        print aa
        print "*" * 8
        print self.csv_by_header
        print set(self.csv_by_header['rundate'])
        print "*" * 8

        a = self.check_headers_presence(reader, required_headers)
        print "self.check_headers_presence(reader)"
        print a
    
        # writer = csv.DictWriter(doc, 
        #                         ["dna_region", "rundate"])
        #                         
        # for row in self.csv_content:
        #     writer.writerow({'dna_region': row.dna_region, 'rundate': row.rundate})
        #     print writer
            


    def parce_csv(self, reader):
      for y_index, row in enumerate(reader):
          self.csv_content.append(row)
          print "self.csv_content 1 = "
          print self.csv_content
          if y_index == 0:
              self.csv_headers = [header_name.lower() for header_name in row if header_name]
              print "self.csv_headers 1 = "
              print self.csv_headers
              continue
      return self.csv_headers, self.csv_content

    def check_headers_presence(self, reader, required_headers):
      missing_headers = set(required_headers) - set([r.lower() for r in self.csv_headers])
      print "missing_headers: "
      print missing_headers
      if missing_headers:
          missing_headers_str = ', '.join(missing_headers)
          # todo: return error_message instead
          raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
      return True

    def required_cell_values_validation(reader):
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
            if self.csv_headers[x_index] in required_headers:
                if not cell_value:
                    raise ValidationError(u'Missing required value %s for row %s' %
                                            (self.csv_headers[x_index], y_index + 1))
    