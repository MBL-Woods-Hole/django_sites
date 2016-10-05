from django.conf.urls import url

from . import views

app_name = 'submission'

urlpatterns = [
    # ex: /submission/
    url(r'^$', views.upload_metadata, name='upload_metadata'),
    url(r'^upload_metadata/$', views.upload_metadata, name='upload_metadata'),
    # url(r'^upload_metadata__run_info_form/$', views.upload_metadata__run_info_form, name='upload_metadata__run_info_form'),
    
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

]
