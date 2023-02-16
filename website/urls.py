from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^search/(?P<page_no>\d+)/$', views.search, name='search'),
    re_path(r'^getavailableslots/$', views.get_availabile_slots, name='getavailableslots'),
    re_path(r'^bookslot/$', views.book_slot, name='bookslot'),
    re_path(r'^viewproperty/(?P<property_id>\d+)/$',views.view_property,name='viewproperty'),
    #re_path(r'^profile/$', views.profile, name='profile'),
    #re_path(r'^postassignment/$', views.post_assignment, name='postassignment'),
    #re_path(r'^findskills/$', views.skills_search, name='findskills'),
	# re_path(r'^createcalendar/$', views.create_calendar, name='createcalendar'),
    # re_path(r'^about/$', views.about, name='about'),
    # re_path(r'^mycalendars/$', views.my_calendars, name='mycalendars'),
    # re_path(r'^calendars/(?P<object_id>\d+)/$', views.view_calendar, name='calendars'),
    # re_path(r'^calendars/delete/(?P<calendar_id>\d+)/$', views.delete_calendar, name='delete'),
    # re_path(r'^sendbyemail/(?P<calendar_id>\d+)/$', views.share_by_email, name='sendbyemail'),
    # re_path(r'^addday/$', views.add_day, name='addday'),
    # re_path(r'^editday/(?P<advent_id>\d+)/$', views.edit_day, name='editday'),
    # #re_path(r'^sendemail/$', views.send_me_email, name='sendemail'),
    # re_path(r'^public/viewcalendar/(?P<calendar_id>\d+)/$', views.view_calendar_public, name='viewcalendar'),
    # re_path(r'^public/viewcalendarday/(?P<calendar_id>\d+)/(?P<day>\d+)/$', views.view_calendar_day_view, name='viewcalendarday'),
]