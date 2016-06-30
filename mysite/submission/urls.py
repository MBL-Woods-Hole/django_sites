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