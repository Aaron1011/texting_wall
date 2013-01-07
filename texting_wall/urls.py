from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index'),
    url(r'^create_account/', 'main.views.create_account'),
    url(r'^finish/', 'main.views.finish'),
    url(r'^login/', 'django.contrib.auth.views.login', kwargs={"template_name": 'login.html'}, name="login"),
    url(r'^logout/', 'main.views.logout_view'),
    url(r'^create_wall/', 'main.views.new_wall'),
    url(r'^recieve_sms/', 'main.views.sms_message', name="recieve_sms"),
    url(r'^wall/(?P<id>\d+)/', 'main.views.display_wall'),
    url(r'^messages/(?P<name>\w+)/', 'main.views.display_messages'),
    url(r'^authorize/(?P<id>\d+)/', 'main.views.twitter_oauth'),
    url(r'^authorize$', 'main.views.twitter_oauth'),
    url(r'^uucmthanks/', redirect_to, {'url': '/messages/uucmthanks/'}),
    url(r'^verify_sms/', 'main.views.verify_sms'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
