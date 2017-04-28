from django.conf.urls import url

from . import views

app_name = 'metadata_template'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^metadata_form/$', views.metadata_form, name='metadata_form'),
]