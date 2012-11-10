from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'texting_wall.views.home', name='home'),
    # url(r'^texting_wall/', include('texting_wall.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index'),
    url(r'^create_account/', 'main.views.create_account'),
    url(r'^finish/', 'main.views.finish'),
    url(r'^login/', 'django.contrib.auth.views.login', kwargs={"template_name": 'login.html'}),
    url(r'^create_wall/', 'main.views.new_wall'),
    url(r'^recieve_sms/', 'main.views.sms_message'),
    url(r'^wall/(?P<id>\d+)/', 'main.views.display_wall'))

