from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'above', views.above, name='above'),
    url(r'below', views.below, name='below'),
    url(r'equal', views.equal, name='equal')
]

