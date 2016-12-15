from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
import logging

from . import views

app_name = 'submission'
logging.debug("""GGG settings.STATIC_URL = %s, 
settings.STATIC_ROOT = %s, 
settings.REPOSITORY_ROOT = %s, 
settings.BASE_DIR = %s""" % (settings.STATIC_URL, settings.STATIC_ROOT, settings.REPOSITORY_ROOT, settings.BASE_DIR))
# /Users/ashipunova/BPC/python_web/django_sites/mysite/static/

urlpatterns = [
    # ex: /submission/
    # url(r'^submissions/illumina/', include([
        url(r'^$', views.upload_metadata, name='upload_metadata'),
        url(r'^upload_metadata/$', views.upload_metadata, name='upload_metadata'),
        url(r'^add_project/$', views.add_project, name='add_project'),

        url(r'^demultiplex/$', views.demultiplex, name='demultiplex'),
        url(r'^overlap/$', views.overlap, name='overlap'),
        url(r'^overlap_only/$', views.overlap_only, name='overlap_only'),
        url(r'^filter_mismatch/$', views.filter_mismatch, name='filter_mismatch'),
        url(r'^uniqueing/$', views.uniqueing, name='uniqueing'),
        url(r'^chimera_checking/$', views.chimera_checking, name='chimera_checking'),
        url(r'^gast/$', views.gast, name='gast'),
        url(r'^run_info_upload/$', views.run_info_upload, name='run_info_upload'),
        url(r'^data_upload/$', views.data_upload, name='data_upload'),
        url(r'^help/$', views.help, name='help'),
        url(r'^gzip_all/$', views.gzip_all, name='gzip_all'),
        url(r'^gunzip_all/$', views.gunzip_all, name='gunzip_all'),
        url(r'^clear_db/$', views.clear_db, name='clear_db'),
        url(r'^check_fa_counts/$', views.check_fa_counts, name='check_fa_counts'),
        url(r'^check_db_counts/$', views.check_db_counts, name='check_db_counts'),
    # ])),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# urlpatterns = [
    # ... the rest of your URLconf goes here ...
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
