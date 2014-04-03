from django.conf.urls import patterns, url
from GR3 import views

urlpatterns = patterns('',
    url(r'^job/', views.get_result),
    url(r'', views.current_datetime),
    

)
