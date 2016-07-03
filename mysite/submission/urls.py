from django.conf.urls import url

from . import views

app_name = 'submission'

urlpatterns = [
    # ex: /submission/
    url(r'^$', views.index, name='index'),
    # ex: /submission/5/
    url(r'^(?P<run_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /submission/5/results/
    url(r'^(?P<run_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /submission/5/vote/
    url(r'^(?P<run_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^help/$', views.help, name='help'),
    url(r'^gzip_all/$', views.gzip_all, name='gzip_all'),
    url(r'^db_upload/$', views.db_upload, name='db_upload'),
    # url(r'^run_info_upload/$', views.run_info_upload, name='run_info_upload'),
    url(r'^run_info_upload/$', views.run_info_upload, name='run_info_upload'),
    # Todo: rm run_info_upload, rename db_upload into a name for both
    url(r'^gast/$', views.gast, name='gast'),
    url(r'^chimera_checking/$', views.chimera_checking, name='chimera_checking'),
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
