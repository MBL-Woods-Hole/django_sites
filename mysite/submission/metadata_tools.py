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
        # self.out_metadata = defaultdict( lambda: defaultdict(int) )
        self.out_metadata = defaultdict( defaultdict )
        self.out_metadata_table = defaultdict( list )
        self.vamps_submissions = {}
        self.user_info_arr = {}
        
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

        self.HEADERS_TO_EDIT_METADATA = ['domain', 'lane', 'contact_name', 'run_key', 'barcode_index', 'adaptor', 'project', 'dataset', 'dataset_description', 'env_source_name', 'tubelabel', 'barcode', 'amp_operator']

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
            dialect = csv.Sniffer().sniff(codecs.EncodedFile(self.csvfile, "utf-8").read(1024), delimiters=',')
        except csv.Error as e:
            self.errors.append('Warning for %s: %s' % (self.csvfile, e))
        except:
            raise
        else:
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

    def run_query_to_dict(self, query):
        res_dict = {}
        cursor = connection.cursor()
        cursor.execute(query)
        
        column_names = [d[0] for d in cursor.description]

        for row in cursor:
          res_dict =  dict(zip(column_names, row))
         
        return res_dict
      # dump it to a json string
      # self.vamps_submissions = json.dumps(info)

    def get_vamps_submission_info(self, db_name = "test_vamps"):
        # todo: get db_name depending on local/not
        out_file_name = "temp_subm_info"
        try:
            for submit_code in self.csv_by_header_uniqued['submit_code']:
                print "submit_code = %s" % submit_code
                query_subm = """SELECT subm.*, auth.user, auth.passwd, auth.first_name, auth.last_name, auth.active, auth.security_level, auth.email, auth.institution, auth.date_added
                    FROM %s.vamps_submissions AS subm
                    JOIN %s.vamps_auth AS auth
                      ON (auth.id = subm.vamps_auth_id)
                    WHERE submit_code = \"%s\"""" % (db_name, db_name, submit_code)
                self.vamps_submissions[submit_code] = self.run_query_to_dict(query_subm)
            print "self.vamps_submissions = %s" % self.vamps_submissions
        except KeyError as e:
            self.cause = e.args[0]
            self.errors.append(self.no_data_message())
        except:
            raise

    def get_user_info(self, db_name = "test_env454"):
        # todo: get db_name depending on local/not
        db_name = "test_env454"
        try:
            for submit_code in self.csv_by_header_uniqued['submit_code']:
                # print "submit_code = %s, self.vamps_submissions[submit_code]['user'] = %s" % (submit_code, self.vamps_submissions[submit_code]['user'])
                vamps_user_id = self.vamps_submissions[submit_code]['user']
                
                query_user = """SELECT contact_id, contact, email, institution, vamps_name, first_name, last_name
                    FROM %s.contact
                    WHERE vamps_name = \"%s\"""" % (db_name, vamps_user_id)
                self.user_info_arr[submit_code] = self.run_query_to_dict(query_user)
            # print "self.user_info_arr = %s" % self.user_info_arr
        except KeyError as e:
            self.cause = e.args[0]
            self.errors.append(self.no_data_message())
        except:
            raise

    def get_selected_variables(self, request_post):
        # change from form if needed
        if 'submit_run_info' in request_post:
            self.selected_machine       = request_post.get('csv_platform', False)
            print "self.selected_machine in request_post= %s" % (self.selected_machine)
            self.selected_machine_short = self.selected_machine
            self.selected_rundate       = request_post.get('csv_rundate', False)
            
        else:
            # print "self.csv_by_header_uniqued['platform']"
            # print self.csv_by_header_uniqued['platform']
            self.selected_machine = " ".join(self.csv_by_header_uniqued['platform']).lower()
            print "self.selected_machine 2 = %s" % self.selected_machine
            machine_shortcuts_choices = dict(models.Machine.MACHINE_SHORTCUTS_CHOICES)
            # print "MMM machine_shortcuts_choices"
            # print machine_shortcuts_choices
            self.selected_machine_short = machine_shortcuts_choices[self.selected_machine]
            # print "self.selected_machine_short 2 = %s" % self.selected_machine_short

            self.selected_rundate = " ".join(self.csv_by_header_uniqued['rundate']).lower()


    def create_path_to_csv(self):
        #/xraid2-2/g454/run_new_pipeline/illumina/miseq_info/20160711
        print "self.selected_machine from create_path_to_csv = %s" % (self.selected_machine)
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

    def edit_out_metadata(self, request):
        # print "FROM edit_out_metadata: request.session['out_metadata']"
        # print request.session['out_metadata']
        
        self.out_metadata = request.session['out_metadata']
                
        for i, v in self.out_metadata.items():
            # print "i = %s" % i 
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

        # print "self.out_metadata = %s" % self.out_metadata
      
    def make_new_out_metadata(self):
        self.get_csv_by_header()
        idx = 0
        print "self.csv_content = %s, len(self.csv_content) = %s" % (self.csv_content, len(self.csv_content))
        print "self.csv_content[0] =  head = %s" % (self.csv_content[0])
        
        print " &&&&&&& list(set(self.csv_content[0]) & set(self.HEADERS_TO_CSV))"
        a = list(set(self.csv_content[0]) & set(self.HEADERS_TO_CSV))
        print a
        # ['barcode_index', 'lane', 'dna_region', 'read_length', 'env_sample_source_id', 'barcode', 'overlap', 'dataset_description', 'adaptor', 'primer_suite', 'insert_size']
        
        print "self.csv_by_header = %s" % self.csv_by_header
        
        self.get_user_info()
        for i in xrange(len(self.csv_content)-1):
            curr_submit_code = self.csv_by_header['submit_code'][i]
            
            # print i
            self.out_metadata[i]['adaptor']				 = self.csv_by_header['adaptor'][i]
            self.out_metadata[i]['amp_operator']		 = self.csv_by_header['op_amp'][i]
            self.out_metadata[i]['barcode']				 = self.csv_by_header['barcode'][i]
            self.out_metadata[i]['barcode_index']		 = self.csv_by_header['barcode_index'][i]
            self.out_metadata[i]['contact_name']         = self.user_info_arr[curr_submit_code]['last_name'] + ', ' + self.user_info_arr[curr_submit_code]['first_name']
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
            # $combined_metadata[$num]["env_sample_source_id"] = $csv_metadata_row["env_sample_source_id"];
            self.out_metadata[i]['env_source_name']      = self.csv_by_header['env_sample_source_id'][i]
            self.out_metadata[i]['first_name']           = self.user_info_arr[curr_submit_code]['first_name']
            self.out_metadata[i]['funding']                = self.vamps_submissions[curr_submit_code]['funding']
            
            # print "self.csv_by_header['submit_code'][i] = %s" % self.csv_by_header['submit_code'][i]
            # print "self.vamps_submissions[curr_submit_code]['institution'] = %s" % self.vamps_submissions[curr_submit_code]['institution']
            
            self.out_metadata[i]['insert_size']			 = self.csv_by_header['insert_size'][i]
            self.out_metadata[i]['institution']			 = self.vamps_submissions[curr_submit_code]['institution']
            self.out_metadata[i]['lane']				 = self.csv_by_header['lane'][i]
            self.out_metadata[i]['last_name']            = self.user_info_arr[curr_submit_code]['last_name']
            # TODO:
            # $combined_metadata[$num]["locked"]             = $session["vamps_submissions_arr"][$csv_metadata_row["submit_code"]]["locked"];
            # $combined_metadata[$num]["num_of_tubes"]       = $session["vamps_submissions_arr"][$csv_metadata_row["submit_code"]]["num_of_tubes"];
            # $combined_metadata[$num]["nnnn"]               = $nnnn;
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
            # try:
            #     self.out_metadata[i]['run_key']                = self.csv_by_header['run_key'][i]
            # except KeyError:
            #     self.out_metadata[i]['run_key']                = ""
            # except:
            #     raise
                
            # TODO: get from session["run_info"]["seq_operator"] (run_info upload)
            # self.out_metadata[i]['seq_operator']       = self.csv_by_header['seq_operator'][i]
            self.out_metadata[i]['tubelabel']			 = self.csv_by_header['tube_label'][i]
     
        print "self.out_metadata = %s" % self.out_metadata

    def make_metadata_table(self):
        self.out_metadata_table['headers'] = self.HEADERS_TO_EDIT_METADATA
        
        for i in xrange(len(self.out_metadata.keys())):
            self.out_metadata_table['rows'].append([])
        
        for r_num, v in self.out_metadata.items():
            for header in self.HEADERS_TO_EDIT_METADATA:
                try:
                    self.out_metadata_table['rows'][int(r_num)].append(self.out_metadata[r_num][header])
                except KeyError, e:
                    print "KeyError, e = %s" % e
                    self.out_metadata_table['rows'][int(r_num)].append("")
                except:
                    raise
        # print "self.out_metadata_table = %s" % self.out_metadata_table

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
