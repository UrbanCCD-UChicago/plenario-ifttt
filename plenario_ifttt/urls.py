"""plenario_ifttt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from plenario_ifttt.ifttt import setup, status
from plenario_ifttt.views import above, below, dropdown_options, equal

# dynamic options
# {{api_url_prefix}}/ifttt/v1/triggers/{{trigger_slug}}/fields/{{trigger_field_slug}}/options

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ifttt/v1/status', status),
    url(r'^ifttt/v1/test/setup', setup),
    url(r'^ifttt/v1/triggers/above/fields/(?P<field>\w+)/options', dropdown_options),
    url(r'^ifttt/v1/triggers/above', above),
    url(r'^ifttt/v1/triggers/below', below),
    url(r'^ifttt/v1/triggers/equal', equal),
]
