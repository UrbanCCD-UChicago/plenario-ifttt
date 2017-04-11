from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'above', views.above, name='above')
]

