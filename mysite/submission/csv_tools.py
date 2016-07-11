from datetime import datetime
from .models import *
import csv

from django.conf import settings
from django.core.exceptions import ValidationError


class CodeCSvModel():
  
    def __init__(self):
      self.HEADERS = {
      'id': {'field':'id', 'required':True},
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
    	'env_sample_source_id': {'field':'env_sample_source_id', 'required':True},																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												    }
    

    codeid = models.SmallIntegerField(primary_key=True)
    remotecode = models.CharField(max_length=32)
    active = models.BooleanField()
    created = models.DateField()
    modified = models.DateField()
    incentiveid = models.CharField(max_length=32)

    class Meta:
        delimiter = ";"
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
      csv_headers = []
      required_headers = [header_name for header_name, values in
                          self.HEADERS.items() if values['required']]
      print "required_headers = "
      print required_headers
      
      for index, row in enumerate(reader):
        print "III index, row"
        print index, row
      
      
      a = self.check_headers_presence(reader, required_headers)
      print "self.check_headers_presence(reader)"
      print a
      for index, row in enumerate(reader):
        print "III index, row"
        print index, row
      

    def check_headers_presence(self, reader, required_headers):
      for y_index, row in enumerate(reader):
          # check that all headers are present
          if y_index == 0:
              # store header_names to sanity check required cells later
              csv_headers = [header_name.lower() for header_name in row if header_name]
              missing_headers = set(required_headers) - set([r.lower() for r in row])
              if missing_headers:
                  missing_headers_str = ', '.join(missing_headers)
                  raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
              continue
          # ignore blank rows
          if not ''.join(str(x) for x in row):
              continue
      return True

    def required_cell_values_validation(row):
      # sanity check required cell values
      for x_index, cell_value in enumerate(row):
          # if indexerror, probably an empty cell past the headers col count
          try:
              csv_headers[x_index]
          except IndexError:
              continue
          if csv_headers[x_index] in required_headers:
              if not cell_value:
                  raise ValidationError(u'Missing required value %s for row %s' %
                                          (csv_headers[x_index], y_index + 1))
    