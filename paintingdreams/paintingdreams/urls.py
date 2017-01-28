from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wholesale_order/', include('wholesale.urls')),
    url(r'^', include('mainapp.urls')),
]

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         url(r'^media/(.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT,
#             'show_indexes': True
#         }),
#     )
#     urlpatterns += patterns('',
#         url(r'^static/(.*)$', 'django.views.static.serve', {
#             'document_root': settings.STATIC_ROOT,
#             'show_indexes': True
#         }),
#     )
