from django.conf.urls import patterns, url, include

from wholesale import views

urlpatterns = patterns('',
    url(r'^summary$', views.summary),
    url(r'^(.*)/summary$', views.summary),
    url(r'^place-order$', views.place_order),
    url(r'^(.*)/place-order$', views.place_order),
    url(r'^(.*)$', views.start)
)

