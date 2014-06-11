from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from leave.views import LeaveTypeAPI, LeaveTypeFormView, HolidayFormView, HolidayAPI
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ola.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/type$', csrf_exempt(LeaveTypeAPI.as_view()), name='leave_type'),
    url(r'^/type/view$', LeaveTypeFormView.as_view(), name='leave_type_form'),
    url(r'^/holiday$', HolidayAPI.as_view(), name='holiday'),
    url(r'^/holiday/view$', HolidayFormView.as_view(), name='holiday_view'),
)
