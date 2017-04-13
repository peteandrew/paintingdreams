from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wholesale_order/', include('wholesale.urls')),
    url(r'^', include('mainapp.urls')),
]
