from django.urls import re_path
from . import views

urlpatterns = [
	re_path(r'^register/$', views.register, name='register'),
	re_path(r'^signin/$', views.signin, name='signin'),
    re_path(r'^login/$', views.signin, name='login'),
	re_path(r'^signout/$', views.signout, name='signout'),
	re_path(r'^forgot/$', views.forgot, name='signout'),
	re_path(r'^confirm/(?P<confirm_code>\w+)/$', views.confirm, name='confirm'),
	re_path(r'^reset/(?P<confirm_code>\w+)/$', views.reset, name='reset'),
]