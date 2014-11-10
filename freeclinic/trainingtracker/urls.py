from django.conf.urls import patterns, url
from trainingtracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_identifier>\d+)$', views.course, name='course'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^nosectionfound/$', views.noSectionFound, name='nosectionfound'),
    url(r'^login/$', views.login, name='login'),
)