from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<id>\d+)$', views.show, name = 'show'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^addreview$', views.addreview, name = 'addreview'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = 'delete'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = 'remove'),
    url(r'^user/(?P<id>\d+)$', views.user, name = 'user'),
]
