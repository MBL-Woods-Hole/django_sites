from django.conf.urls import url

from . import views

app_name = 'submission'

urlpatterns = [
    # ex: /submission/
    url(r'^$', views.index, name='index'),
    url(r'^metadata_upload/$', views.metadata_upload, name='metadata_upload'),
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
    url(r'^db_cnts/$', views.db_cnts, name='db_cnts'),
    url(r'^files_cnts/$', views.files_cnts, name='files_cnts'),
]

# from django.conf.urls import url
#
# from . import views
#
# app_name = 'submission'
# urlpatterns = [
#     url(r'^$', views.IndexView.as_view(), name='index'),
#     url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#     url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#     url(r'^(?P<run_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]
