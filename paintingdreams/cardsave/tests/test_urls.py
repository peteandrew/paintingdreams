from django.conf.urls import url

from cardsave import views

urlpatterns = [
    url(r'^cardsave-result/$', views.cardsave_result, name="cardsave-result")
]
