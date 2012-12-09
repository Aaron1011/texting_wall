from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

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
    url(r'^logout/', 'main.views.logout_view'),
    url(r'^create_wall/', 'main.views.new_wall'),
    url(r'^recieve_sms/', 'main.views.sms_message'),
    url(r'^wall/(?P<id>\d+)/', 'main.views.display_wall'),
    url(r'^messages/(?P<name>\w+)/', 'main.views.display_messages'),
    url(r'^authorize/(?P<id>\d+)/', 'main.views.twitter_oauth'),
    url(r'^authorize$', 'main.views.twitter_oauth'),
    url(r'^uucmthanks/', redirect_to, {'url': '/messages/uucmthanks/'}),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)

urlpatterns += staticfiles_urlpatterns()
