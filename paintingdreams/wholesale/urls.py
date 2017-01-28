from django.conf.urls import url, include

from wholesale import views

urlpatterns = [
    url(r'^summary$', views.summary),
    url(r'^(.*)/summary$', views.summary),
    url(r'^place-order$', views.place_order),
    url(r'^(.*)/place-order$', views.place_order),
    url(r'^(.*)$', views.start)
]
