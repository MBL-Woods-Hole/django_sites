import models
from .utils import Utils, Dirs
import models_l_env454
from django.forms.models import model_to_dict
from django.db import connection, transaction
import time


def test_choices_not_fetched_when_not_rendering(self):
        initial_queries = len(connection.queries)
        project_query = Project.cache_all_method.all().order_by('project')
        project = ModelChoiceField(queryset = project_query, empty_label = None, to_field_name = 'project')
        field = ModelChoiceField(Group.objects.order_by('-name'))
        self.assertEqual('a', field.clean(self.groups[0].pk).name)
        # only one query is required to pull the model from DB
        self.assertEqual(initial_queries+1, len(connection.queries))