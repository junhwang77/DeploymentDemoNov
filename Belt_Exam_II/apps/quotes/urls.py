from django.conf.urls import url
from . import views
#from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^create$', views.create, name = 'create'),
    url(r'^join$', views.join, name = 'join'),
    url(r'^remove$', views.remove, name = 'remove'),
    url(r'^show/(?P<id>\d+)$', views.show, name = 'show'),
]
