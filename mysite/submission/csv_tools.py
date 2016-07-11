from datetime import datetime
# from adaptor.fields import *
# GroupedCsvModel, CsvFieldDataException
from .models import *

class CodeCSvModel():

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