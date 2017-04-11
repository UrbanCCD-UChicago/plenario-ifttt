from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'setup', views.setup, name='setup'),
]