from django.conf.urls import patterns, url
from trainingtracker import views
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^takeshift/(?P<shift_identifier>\d+)$', views.takeshift, name='takeshift'),
    url(r'^course/(?P<course_identifier>\d+)$', views.course, name='course'),
    url(r'^settings/$', views.Settings.as_view(), name='settings'),
    url(r'^nosectionfound/$', views.noSectionFound, name='nosectionfound'),
    # I rename the template so we don't need a basically empty 'registration' directory
    url(r'^login/$', auth_views.login, {'template_name': 'bfctraining/login.html'}),
    url(r'^logout/$', views.logout_view, name='logout'),
    # url(r'^user/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name='user_update')
)