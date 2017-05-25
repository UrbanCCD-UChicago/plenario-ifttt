from django.conf.urls import include, url
from django.contrib import admin
from plenario_ifttt.ifttt import setup, status
from plenario_ifttt.views import alert, options


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ifttt/v1/status', status),
    url(r'^ifttt/v1/test/setup', setup),
    url(r'^ifttt/v1/triggers/alert/fields/(?P<field>\w+)/options', options),
    url(r'^ifttt/v1/triggers/alert', alert),
]
