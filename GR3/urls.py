from django.conf.urls import patterns, url
from GR3 import views

urlpatterns = patterns('',
    url(r'^$', views.current_datetime),
)
