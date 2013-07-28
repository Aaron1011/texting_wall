from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


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
    url(r'^uucmthanks/', RedirectView.as_view(url='/messages/uucmthanks/')),
    url(r'^create_sms_sender/', 'main.views.create_sms_sender'),
    url(r'^verify_sms/', 'main.views.verify_sms'),
    url(r'^close_wall/', 'main.views.close_wall'),
    url(r'^ping_wall/', 'main.views.ping_wall'))

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
