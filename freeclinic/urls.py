from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'freeclinic.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('trainingtracker.urls', namespace='trainingtracker')),
    #url(r'^courses/', include('trainingtracker.urls', namespace='trainingtracker')),
    url(r'^admin/', include(admin.site.urls)),
    # Need to include this so we can reverse the url in the login template
    url('', include('django.contrib.auth.urls')),
)
